from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from UI.tabs.SettingsTab import SettingsTab
from .ResultTabsWidget import ResultTabsWidget
from .ActionBarWidget import ActionBarWidget
from threads import CLOComparisonThread
import pandas as pd
from utils import extract_clos
import re
import os


class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TRACE")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize the Settings tab
        self.settings_tab = SettingsTab(self)

        # Create Action Bar Widget
        self.action_bar_widget = ActionBarWidget(self)

        # Result Tabs Widget
        self.result_tabs_widget = ResultTabsWidget(self)

        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.settings_tab)  # Add the settings tab directly
        main_layout.addWidget(self.action_bar_widget)  # Add action bar widget
        main_layout.addWidget(self.result_tabs_widget)  # Add results display widget

        # Set up the main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.action_bar_widget.button_compare.clicked.connect(self.compare_clos)
        self.settings_tab.file_selection_widget.update_files_signal.connect(
            self.action_bar_widget.update_file_paths
        )

    def compare_clos(self):
        # Get file paths from the UI
        file_path_existing = self.settings_tab.file_selection_widget.entry_existing.text()
        file_path_new = self.settings_tab.file_selection_widget.entry_new.text()

        # Validate if both file paths are provided
        if not file_path_existing or not file_path_new:
            self.action_bar_widget.show_error_message("File Missing", "Please ensure both file paths are provided.")
            return

        # Validate file existence
        if not os.path.exists(file_path_existing) or not os.path.exists(file_path_new):
            self.action_bar_widget.show_error_message("File Not Found", "One or both of the selected files do not exist.")
            return

        try:
            # Attempt to read the existing file
            excel_file_existing = pd.read_excel(file_path_existing, sheet_name=None)
        except Exception as e:
            # Handle errors while reading the existing file
            self.action_bar_widget.show_error_message("File Read Error", f"Could not read the existing file: {str(e)}")
            return

        try:
            # Attempt to read the new file
            new_clo_data = pd.read_excel(file_path_new)
        except Exception as e:
            # Handle errors while reading the new file
            self.action_bar_widget.show_error_message("File Read Error", f"Could not read the new file: {str(e)}")
            return

        # Check for CLO extraction in the existing file
        existing_clo_dict = {}
        course_pattern = r"^[A-Z]{4,5}\s?\d{4}.*|^[A-Z]{3}\s?\d{4}.*"
        for sheet_name, sheet_data in excel_file_existing.items():
            if re.match(course_pattern, sheet_name):
                if len(sheet_data) >= 13:
                    row_13 = sheet_data.iloc[12]
                    if any(
                        row_13.astype(str).str.contains(
                            "CLO|Course Learning Outcomes", case=False, na=False
                        )
                    ):
                        existing_clo_dict[sheet_name] = extract_clos(sheet_data)

        # If no CLOs were extracted from the existing file, show an error message
        if not existing_clo_dict:
            self.action_bar_widget.show_error_message("CLO Extraction Error", "No CLOs were found in the existing file.")
            return

        # Extract CLOs from the new file
        new_clo_list = extract_clos(new_clo_data)
        if not new_clo_list:  # If no CLOs were found in the new file, show an error message
            self.action_bar_widget.show_error_message("CLO Extraction Error", "No CLOs were found in the new file.")
            return

        # Split existing CLOs into batches for processing
        batch_size = 5
        batches = [
            list(existing_clo_dict.items())[i: i + batch_size]
            for i in range(0, len(existing_clo_dict), batch_size)
        ]

        # Retrieve threshold values
        threshold = self.settings_tab.threshold_widget.threshold_slider.value() / 100
        avg_similarity_threshold = (
            self.settings_tab.threshold_widget.avg_similarity_slider.value() / 100
        )

        try:
            # Start the comparison in a separate thread
            self.thread = CLOComparisonThread(
                existing_clo_dict, new_clo_list, batches, threshold
            )
            self.thread.update_progress.connect(self.update_progress)
            self.thread.comparison_done.connect(self.display_results)
            self.thread.start()

        except Exception as e:
            # Handle any errors that occur during the comparison process
            self.action_bar_widget.show_error_message("Comparison Error", f"An error occurred during the CLO comparison: {str(e)}")

    def update_progress(self, value):
        """Update progress bar."""
        self.action_bar_widget.progressbar.setValue(value)

    def display_results(self, results):
        """Display results in the ResultTabsWidget."""
        # Retrieve threshold values for similarity
        threshold = self.settings_tab.threshold_widget.threshold_slider.value() / 100
        avg_threshold = (
            self.settings_tab.threshold_widget.avg_similarity_slider.value() / 100
        )

        # Prepare data for displaying in the table
        results_for_table = []
        for sheet_name, average_similarity, highest_similarity_pairs in results:
            results_for_table.append((sheet_name, average_similarity))

        # Update the ResultTabsWidget with the comparison results
        self.result_tabs_widget.display_results(results, threshold, avg_threshold)

        # Update results in the SettingsTab (tabular format)
        self.settings_tab.update_results(results_for_table)
