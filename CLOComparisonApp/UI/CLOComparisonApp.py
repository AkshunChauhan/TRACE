from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QToolBar, QAction
from PyQt5.QtCore import Qt
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

        # Add a toolbar with Help and About actions
        self.add_toolbar()

        # Connections
        self.action_bar_widget.button_compare.clicked.connect(self.compare_clos)
        self.settings_tab.file_selection_widget.update_files_signal.connect(
            self.action_bar_widget.update_file_paths
        )

    def add_toolbar(self):
        """Add a toolbar with Help and About buttons."""
        toolbar = QToolBar("Toolbar", self)
        toolbar.setMovable(False)  # Make the toolbar static

        # Create Help action
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help_popup)
        
        # Create About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_popup)

        # Add actions to the toolbar
        toolbar.addAction(help_action)
        toolbar.addAction(about_action)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def show_help_popup(self):
        """Show a popup box with instructions on how to use the application."""
        instructions = (
            "Welcome to the TRACE application!\n\n"
            "Step 1: Select the existing files, then the new file.\n"
            "Step 2: Set the thresholds using the sliders.\n"
            "Step 3: Hit the 'Start Compare' button to begin the comparison process.\n\n"
            "Note:\n"
            "- The application may take some time to run based on your system specifications.\n"
            "- In the existing file, ensure that one Excel file contains all the sheets that need to be compared.\n"
            "- In the new file, ensure it contains only one sheet. All sheets must follow the standard structure.\n\n"
            "Thresholds:\n"
            "- The first threshold is the 'low-level threshold,' which specifies the percentage match required for each sentence.\n"
            "- The second threshold is the 'high-level threshold,' which checks the average similarity of the entire sheet (usually containing 5 to 6 CLOs).\n\n"
            "If the application crashes or the comparison process takes too long, please contact the developer at:\n"
            "akshun.chauhan@rdpolytech.ca"
        )
        QMessageBox.information(self, "Help", instructions)


    def show_about_popup(self):
        """Show a popup box with information about the application."""
        about_text = (
            "<p>TRACE stands for <b>Total Recognition and Course Evaluation</b>. It is an internal tool specifically designed to identify duplications in courses using Course Learning Outcomes (CLOs). "
            "This innovative application leverages machine learning to analyze and find similarities between sentences, utilizing the <i>all-MiniLM-L6-v2</i> sentence transformer model.</p>"
            "\n\n"
            "<p>As a prototype, TRACE is adaptable and can be further modified to meet specific needs. It was developed as a capstone project by <b>Akshun Chauhan</b> under the supervision of "
            "<b>Dr. Rashid jalal Qureshi</b>.</p>"
            "\n\n"
            "<p>To learn more about the project or view the source code, visit the following links:</p>"
            "<ul>"
            "<li><a href='https://github.com/AkshunChauhan/TRACE.git'>GitHub: github.com/AkshunChauhan/TRACE.git</a></li>"
            "<li><a href='https://www.linkedin.com/in/akshunchauhan/'>LinkedIn: linkedin.com/in/akshunchauhan/</a></li>"
            "</ul>"
        )

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About TRACE")
        msg_box.setTextFormat(Qt.RichText)  # Enables HTML formatting
        msg_box.setText(about_text)
        msg_box.exec_()


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
