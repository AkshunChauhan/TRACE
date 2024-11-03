from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from UI.tabs.FileTab import FileTab
from UI.tabs.SettingsTab import SettingsTab
from UI.tabs.HelpTab import HelpTab
from UI.tabs.AboutTab import AboutTab
from .ResultTabsWidget import ResultTabsWidget
from .ActionBarWidget import ActionBarWidget
from threads import CLOComparisonThread
import pandas as pd
from utils import extract_clos
import re

class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TRACE")
        self.setGeometry(100, 100, 900, 700)

        # Create the tab widget
        self.tab_widget = QTabWidget()

        # Initialize each tab
        self.tab_file = FileTab(self)
        self.tab_settings = SettingsTab(self)
        self.tab_help = HelpTab(self)
        self.tab_about = AboutTab(self)

        # Add the tabs to the tab widget
        self.tab_widget.addTab(self.tab_file, "File")
        self.tab_widget.addTab(self.tab_settings, "Settings")
        self.tab_widget.addTab(self.tab_help, "Help")
        self.tab_widget.addTab(self.tab_about, "About")

        # Create Action Bar Widget
        self.action_bar_widget = ActionBarWidget(self)

        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.action_bar_widget)

        # Result Tabs Widget
        self.result_tabs_widget = ResultTabsWidget(self)
        main_layout.addWidget(self.result_tabs_widget)

        # Set up the main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connections
        self.action_bar_widget.button_compare.clicked.connect(self.compare_clos)
        # Assuming FileSelectionWidget in SettingsTab sends update_files_signal
        self.tab_settings.file_selection_widget.update_files_signal.connect(
            self.action_bar_widget.update_file_paths
        )

    def close_help(self):
        self.tab_widget.setCurrentIndex(0)  # Return to the first tab (File tab) or adjust as needed

    def close_about(self):
        self.tab_widget.setCurrentIndex(0)  # Return to the first tab (File tab) or adjust as needed

    def compare_clos(self):
        file_path_existing = self.tab_settings.file_selection_widget.entry_existing.text()
        file_path_new = self.tab_settings.file_selection_widget.entry_new.text()
        
        if not file_path_existing or not file_path_new:
            self.result_tabs_widget.result_tab.setPlainText("Please select both files.")
            return

        existing_clo_dict = {}
        excel_file_existing = pd.read_excel(file_path_existing, sheet_name=None)
        new_clo_data = pd.read_excel(file_path_new)
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

        new_clo_list = extract_clos(new_clo_data)
        batch_size = 5
        batches = [
            list(existing_clo_dict.items())[i: i + batch_size]
            for i in range(0, len(existing_clo_dict), batch_size)
        ]

        threshold = self.tab_settings.threshold_widget.threshold_slider.value() / 100
        self.avg_similarity_threshold = self.tab_settings.threshold_widget.avg_similarity_slider.value() / 100

        self.thread = CLOComparisonThread(
            existing_clo_dict, new_clo_list, batches, threshold
        )
        self.thread.update_progress.connect(self.update_progress)
        self.thread.comparison_done.connect(self.display_results)
        self.thread.start()

    def update_progress(self, value):
        self.action_bar_widget.progressbar.setValue(value)

    def display_results(self, results):
        threshold = self.tab_settings.threshold_widget.threshold_slider.value() / 100
        avg_threshold = self.tab_settings.threshold_widget.avg_similarity_slider.value() / 100
        self.result_tabs_widget.display_results(results, threshold, avg_threshold)
