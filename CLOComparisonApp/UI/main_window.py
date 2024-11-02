import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QTabWidget,
    QTextEdit,
    QHBoxLayout,
    QProgressBar,
    QPushButton,
)
from PyQt5.QtCore import Qt
from UI.components import create_file_selection_group, create_threshold_group
from UI.helpers import update_progress, display_results
from threads import CLOComparisonThread
import pandas as pd


class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CLO Comparison Tool")
        self.setGeometry(100, 100, 900, 700)

        main_layout = QVBoxLayout()

        # Step 1: File Selection Group
        self.entry_existing, self.entry_new, file_selection_group = (
            create_file_selection_group(self)
        )
        main_layout.addWidget(file_selection_group)

        # Step 2 & 3: Threshold Group
        self.threshold_slider, self.avg_similarity_slider, threshold_group = (
            create_threshold_group(self)
        )
        main_layout.addWidget(threshold_group)

        # Action Layout with Compare Button and Progress Bar
        action_layout = QHBoxLayout()
        self.button_compare = QPushButton("Compare CLOs", self)
        self.button_compare.clicked.connect(self.compare_clos)
        self.progressbar = QProgressBar(self)
        action_layout.addWidget(self.button_compare)
        action_layout.addWidget(self.progressbar)
        main_layout.addLayout(action_layout)

        # Tabs for displaying results
        self.tabs = QTabWidget()
        self.result_tab = QTextEdit()
        self.match_tab = QTextEdit()
        self.no_match_tab = QTextEdit()
        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        main_layout.addWidget(self.tabs)

        # Spacer for layout expansion
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)

        # Set up the main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def compare_clos(self):
        file_path_existing = self.entry_existing.text()
        file_path_new = self.entry_new.text()
        if not file_path_existing or not file_path_new:
            self.result_tab.setPlainText("Please select both files.")
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
        threshold = self.threshold_slider.value() / 100
        self.avg_similarity_threshold = self.avg_similarity_slider.value() / 100

        self.thread = CLOComparisonThread(existing_clo_dict, new_clo_list, threshold)
        self.thread.update_progress.connect(lambda value: update_progress(self, value))
        self.thread.comparison_done.connect(
            lambda results: display_results(
                self, results, self.avg_similarity_threshold
            )
        )
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CLOComparisonApp()
    window.show()
    sys.exit(app.exec_())
