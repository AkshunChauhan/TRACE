from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QProgressBar,
    QFileDialog,
    QTextEdit,
    QLabel,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QTabWidget,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
)
from PyQt5.QtCore import pyqtSignal
import pandas as pd
from threads import CLOComparisonThread
from utils import extract_clos
import re


class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CLO Comparison Tool")
        self.setGeometry(100, 100, 900, 700)
        main_layout = QVBoxLayout()
        file_selection_group = QGroupBox("Step 1: Select Files")
        file_layout = QFormLayout()
        self.entry_existing = QLineEdit(self)
        self.button_existing = QPushButton("Browse", self)
        self.button_existing.clicked.connect(lambda: self.select_file("existing"))
        self.entry_new = QLineEdit(self)
        self.button_new = QPushButton("Browse", self)
        self.button_new.clicked.connect(lambda: self.select_file("new"))
        file_layout.addRow(QLabel("Existing Excel File:"), self.entry_existing)
        file_layout.addRow("", self.button_existing)
        file_layout.addRow(QLabel("New Excel File:"), self.entry_new)
        file_layout.addRow("", self.button_new)
        file_selection_group.setLayout(file_layout)
        main_layout.addWidget(file_selection_group)

        action_layout = QHBoxLayout()
        self.button_compare = QPushButton("Compare CLOs", self)
        self.button_compare.clicked.connect(self.compare_clos)
        self.progressbar = QProgressBar(self)
        action_layout.addWidget(self.button_compare)
        action_layout.addWidget(self.progressbar)
        main_layout.addLayout(action_layout)

        self.tabs = QTabWidget()
        self.result_tab = QTextEdit()
        self.match_tab = QTextEdit()
        self.no_match_tab = QTextEdit()
        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        main_layout.addWidget(self.tabs)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.setStyleSheet(
            """
            QMainWindow { background-color: #f5f5f5; }
            QPushButton { padding: 10px; font-size: 14px; }
            QLineEdit { padding: 8px; font-size: 14px; }
            QProgressBar { height: 25px; }
            QTextEdit { font-size: 14px; padding: 10px; }
            QLabel { font-weight: bold; }
            QGroupBox { font-size: 14px; padding: 15px; border: 1px solid #b0b0b0; border-radius: 10px; }
            QTabWidget::pane { border: 1px solid #b0b0b0; }
        """
        )

    def select_file(self, file_type):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_type == "existing":
            self.entry_existing.setText(file_path)
        else:
            self.entry_new.setText(file_path)

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
        batch_size = 5
        batches = [
            list(existing_clo_dict.items())[i : i + batch_size]
            for i in range(0, len(existing_clo_dict), batch_size)
        ]
        self.thread = CLOComparisonThread(existing_clo_dict, new_clo_list, batches)
        self.thread.update_progress.connect(self.update_progress)
        self.thread.comparison_done.connect(self.display_results)
        self.thread.start()

    def update_progress(self, value):
        self.progressbar.setValue(value)

    def display_results(self, results):
        overall_result_text = ""
        match_result_text = ""
        no_match_result_text = ""
        for sheet_name, average_similarity, highest_similarity_pairs in results:
            overall_result_text += (
                f"Course: {sheet_name}, Average Similarity: {average_similarity:.2f}\n"
            )
            if average_similarity >= 0.5:
                match_result_text += f"\nMatching Course: {sheet_name}\n"
                for existing_clo, new_clo, score in highest_similarity_pairs:
                    match_result_text += f"  Existing CLO: {existing_clo}\n  New CLO: {new_clo}\n  Similarity Score: {score:.2f}\n"
            else:
                no_match_result_text += f"No match found for course: {sheet_name}\n"
        self.result_tab.setPlainText(overall_result_text)
        self.match_tab.setPlainText(match_result_text)
        self.no_match_tab.setPlainText(no_match_result_text)
