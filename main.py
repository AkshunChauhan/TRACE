import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar, QFileDialog, QTextEdit,
    QLabel, QLineEdit, QGroupBox, QFormLayout, QTabWidget, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import re
import torch
from sentence_transformers import SentenceTransformer, util

# Initialize Sentence-BERT model
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('bert-large-nli-mean-tokens')
model.to(device)


def jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity between two sets."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0
    return intersection / union


def extract_clos(data, start_row=12, start_col=1, end_col=None):
    """Extract Course Learning Outcomes (CLOs) from Excel data."""
    clo_list = []
    for i in range(start_row, len(data)):
        row = data.iloc[i]
        if not row.isnull().all():
            non_nan_values = row.dropna()
            if len(non_nan_values) > 1:
                clo_descriptions = non_nan_values[start_col:end_col].tolist()
                filtered_descriptions = [desc for desc in clo_descriptions if not re.match(r'^[C]\d+$', str(desc))]
                clo_list.extend(filtered_descriptions)
        else:
            break
    return clo_list


class CLOComparisonThread(QThread):
    update_progress = pyqtSignal(int)
    comparison_done = pyqtSignal(list)

    def __init__(self, existing_clo_dict, new_clo_list, batches):
        super().__init__()
        self.existing_clo_dict = existing_clo_dict
        self.new_clo_list = new_clo_list
        self.batches = batches

    def run(self):
        results = []
        for batch_index, batch in enumerate(self.batches):
            results.extend(self.process_batch(batch, self.existing_clo_dict, self.new_clo_list))
            self.update_progress.emit(int((batch_index + 1) / len(self.batches) * 100))
        self.comparison_done.emit(results)

    def process_batch(self, batch, existing_clo_dict, new_clo_list):
        """Process a batch of course sheets."""
        results = []
        for sheet_name, existing_clo_set in batch:
            existing_clo_embeddings = model.encode(existing_clo_set, batch_size=8, convert_to_tensor=True)
            new_clo_embeddings = model.encode(new_clo_list, batch_size=8, convert_to_tensor=True)

            # Calculate semantic similarity
            semantic_similarities = util.cos_sim(existing_clo_embeddings, new_clo_embeddings)
            threshold = 0.7
            highest_similarity_pairs = []

            for i, existing_clo in enumerate(existing_clo_set):
                for j, new_clo in enumerate(new_clo_list):
                    similarity_score = semantic_similarities[i][j].item()
                    if similarity_score > threshold:
                        highest_similarity_pairs.append((existing_clo, new_clo, similarity_score))

            average_semantic_similarity = (semantic_similarities > threshold).float().mean().item()

            # Calculate Jaccard similarity
            existing_clo_set = set(existing_clo_set)
            new_clo_set = set(new_clo_list)
            average_jaccard_similarity = jaccard_similarity(existing_clo_set, new_clo_set)

            # Combine similarities
            average_similarity = (average_semantic_similarity + average_jaccard_similarity) / 2

            # Store result
            results.append((sheet_name, average_similarity, highest_similarity_pairs))

        return results


class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CLO Comparison Tool')
        self.setGeometry(100, 100, 900, 700)

        # Main Layout
        main_layout = QVBoxLayout()

        # Group Box for File Selection
        file_selection_group = QGroupBox("Step 1: Select Files")
        file_layout = QFormLayout()

        # Existing file selection
        self.entry_existing = QLineEdit(self)
        self.button_existing = QPushButton("Browse", self)
        self.button_existing.clicked.connect(lambda: self.select_file('existing'))

        # New file selection
        self.entry_new = QLineEdit(self)
        self.button_new = QPushButton("Browse", self)
        self.button_new.clicked.connect(lambda: self.select_file('new'))

        # Add file selection to form layout
        file_layout.addRow(QLabel("Existing Excel File:"), self.entry_existing)
        file_layout.addRow("", self.button_existing)
        file_layout.addRow(QLabel("New Excel File:"), self.entry_new)
        file_layout.addRow("", self.button_new)
        file_selection_group.setLayout(file_layout)
        main_layout.addWidget(file_selection_group)

        # Compare Button and Progress Bar
        action_layout = QHBoxLayout()
        self.button_compare = QPushButton('Compare CLOs', self)
        self.button_compare.clicked.connect(self.compare_clos)
        self.progressbar = QProgressBar(self)

        action_layout.addWidget(self.button_compare)
        action_layout.addWidget(self.progressbar)
        main_layout.addLayout(action_layout)

        # Tab Widget for Results
        self.tabs = QTabWidget()
        self.result_tab = QTextEdit()
        self.match_tab = QTextEdit()
        self.no_match_tab = QTextEdit()

        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        main_layout.addWidget(self.tabs)

        # Add Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)

        # Apply main layout to the window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Style the widgets for a modern look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
            }
            QProgressBar {
                height: 25px;
            }
            QTextEdit {
                font-size: 14px;
                padding: 10px;
            }
            QLabel {
                font-weight: bold;
            }
            QGroupBox {
                font-size: 14px;
                padding: 15px;
                border: 1px solid #b0b0b0;
                border-radius: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #b0b0b0;
            }
        """)

    def select_file(self, file_type):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_type == 'existing':
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

        course_pattern = r'^[A-Z]{4,5}\s?\d{4}.*|^[A-Z]{3}\s?\d{4}.*'

        for sheet_name, sheet_data in excel_file_existing.items():
            if re.match(course_pattern, sheet_name):
                if len(sheet_data) >= 13:
                    row_13 = sheet_data.iloc[12]
                    if any(row_13.astype(str).str.contains('CLO|Course Learning Outcomes', case=False, na=False)):
                        existing_clo_dict[sheet_name] = extract_clos(sheet_data)

        new_clo_list = extract_clos(new_clo_data)

        # Split into batches
        batch_size = 5
        batches = [list(existing_clo_dict.items())[i:i + batch_size] for i in range(0, len(existing_clo_dict), batch_size)]

        # Create and start comparison thread
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
            overall_result_text += f"Course: {sheet_name}, Average Similarity: {average_similarity:.2f}\n"
            if average_similarity >= 0.5:
                match_result_text += f"\nMatching Course: {sheet_name}\n"
                for existing_clo, new_clo, score in highest_similarity_pairs:
                    match_result_text += f"  Existing CLO: {existing_clo}\n  New CLO: {new_clo}\n  Similarity Score: {score:.2f}\n"
            else:
                no_match_result_text += f"No match found for course: {sheet_name}\n"

        self.result_tab.setPlainText(overall_result_text)
        self.match_tab.setPlainText(match_result_text)
        self.no_match_tab.setPlainText(no_match_result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CLOComparisonApp()
    window.show()
    sys.exit(app.exec_())
