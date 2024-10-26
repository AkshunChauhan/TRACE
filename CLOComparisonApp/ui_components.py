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
    QSlider,
)
from PyQt5.QtCore import Qt, pyqtSignal
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

        # Step 1: Select Files
        file_selection_group = QGroupBox("Step 1: Select Files")
        file_selection_layout = QHBoxLayout()

        # Existing File Section
        existing_file_layout = QFormLayout()
        self.entry_existing = QLineEdit(self)
        self.button_existing = QPushButton("Browse", self)
        self.button_existing.clicked.connect(lambda: self.select_file("existing"))
        existing_file_layout.addRow(QLabel("Existing Excel File:"), self.entry_existing)
        existing_file_layout.addRow("", self.button_existing)

        # New File Section
        new_file_layout = QFormLayout()
        self.entry_new = QLineEdit(self)
        self.button_new = QPushButton("Browse", self)
        self.button_new.clicked.connect(lambda: self.select_file("new"))
        new_file_layout.addRow(QLabel("New Excel File:"), self.entry_new)
        new_file_layout.addRow("", self.button_new)

        # Add both layouts to the horizontal layout
        file_selection_layout.addLayout(existing_file_layout)
        file_selection_layout.addLayout(new_file_layout)
        file_selection_group.setLayout(file_selection_layout)
        main_layout.addWidget(file_selection_group)

        # Step 2 & 3: Set Similarity Thresholds
        threshold_group = QGroupBox("Step 2 & 3: Set Similarity Thresholds")
        threshold_layout = QHBoxLayout()

        # Similarity Threshold Slider
        similarity_layout = QVBoxLayout()
        self.threshold_label = QLabel("Similarity Threshold: 0.5", self)
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 100)
        self.threshold_slider.setValue(50)
        self.threshold_slider.valueChanged.connect(self.update_threshold_label)
        similarity_layout.addWidget(self.threshold_label)
        similarity_layout.addWidget(self.threshold_slider)

        # Average Similarity Threshold Slider
        avg_similarity_layout = QVBoxLayout()
        self.avg_similarity_label = QLabel("Average Similarity Threshold: 0.5", self)
        self.avg_similarity_slider = QSlider(Qt.Horizontal)
        self.avg_similarity_slider.setRange(0, 100)
        self.avg_similarity_slider.setValue(50)
        self.avg_similarity_slider.valueChanged.connect(
            self.update_avg_similarity_label
        )
        avg_similarity_layout.addWidget(self.avg_similarity_label)
        avg_similarity_layout.addWidget(self.avg_similarity_slider)

        # Add both sliders to the threshold layout side-by-side
        threshold_layout.addLayout(similarity_layout)
        threshold_layout.addLayout(avg_similarity_layout)
        threshold_group.setLayout(threshold_layout)
        main_layout.addWidget(threshold_group)

        # Action Layout with Compare button and Progress Bar
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
        self.setStyleSheet(
            """
            QMainWindow { background-color: #ffffff; }
            QPushButton { padding: 10px; font-size: 14px; }
            QLineEdit { padding: 8px; font-size: 14px; }
            QProgressBar { height: 25px; }
            QTextEdit { font-size: 14px; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; }
            QLabel { font-weight: bold; color: #333; }
            QGroupBox { font-size: 14px; padding: 15px; border: 1px solid #b0b0b0; border-radius: 10px; margin-top: 10px; }
            QSlider::groove:horizontal { height: 6px; background: #e0e0e0; }
            QSlider::handle:horizontal { background: #3399ff; width: 14px; border-radius: 7px; }
            QTabWidget::pane { border: 1px solid #b0b0b0; }
        """
        )

    def update_threshold_label(self):
        threshold_value = self.threshold_slider.value() / 100
        self.threshold_label.setText(f"Similarity Threshold: {threshold_value:.2f}")

    def update_avg_similarity_label(self):
        avg_similarity_value = self.avg_similarity_slider.value() / 100
        self.avg_similarity_label.setText(
            f"Average Similarity Threshold: {avg_similarity_value:.2f}"
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

        threshold = self.threshold_slider.value() / 100
        self.avg_similarity_threshold = self.avg_similarity_slider.value() / 100

        self.thread = CLOComparisonThread(
            existing_clo_dict, new_clo_list, batches, threshold
        )
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
            if average_similarity >= self.avg_similarity_threshold:
                match_result_text += f"\nMatching Course: {sheet_name}\n"
                for existing_clo, new_clo, score in highest_similarity_pairs:
                    match_result_text += f"  Existing CLO: {existing_clo}\n  New CLO: {new_clo}\n  Similarity Score: {score:.2f}\n"
            else:
                no_match_result_text += f"No match found for course: {sheet_name}\n"
        self.result_tab.setPlainText(overall_result_text)
        self.match_tab.setPlainText(match_result_text)
        self.no_match_tab.setPlainText(no_match_result_text)
