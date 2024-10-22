from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QGroupBox, QFormLayout,
    QLineEdit, QPushButton, QLabel, QProgressBar,
    QHBoxLayout, QTabWidget, QTextEdit, QWidget,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from app.services.batch_processor import CLOComparisonThread
from app.utils.file_utils import select_file

class CLOComparisonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CLO Comparison Tool')
        self.setGeometry(100, 100, 900, 700)

        main_layout = QVBoxLayout()

        # File selection group
        file_selection_group = QGroupBox("Step 1: Select Files")
        file_layout = QHBoxLayout()  # Use a horizontal layout for side by side

        # Existing file selection
        self.entry_existing = QLineEdit(self)
        self.button_existing = QPushButton("Browse", self)
        self.button_existing.clicked.connect(lambda: select_file(self, 'existing', self.entry_existing))
        
        existing_layout = QVBoxLayout()  # Vertical layout for existing file
        existing_layout.addWidget(QLabel("Existing Excel File:"))
        existing_layout.addWidget(self.entry_existing)
        existing_layout.addWidget(self.button_existing)

        # New file selection
        self.entry_new = QLineEdit(self)
        self.button_new = QPushButton("Browse", self)
        self.button_new.clicked.connect(lambda: select_file(self, 'new', self.entry_new))
        
        new_layout = QVBoxLayout()  # Vertical layout for new file
        new_layout.addWidget(QLabel("New Excel File:"))
        new_layout.addWidget(self.entry_new)
        new_layout.addWidget(self.button_new)

        # Add both vertical layouts to the horizontal layout
        file_layout.addLayout(existing_layout)
        file_layout.addLayout(new_layout)
        
        file_selection_group.setLayout(file_layout)
        main_layout.addWidget(file_selection_group)

        # Action layout
        action_layout = QHBoxLayout()
        self.button_compare = QPushButton('Compare CLOs', self)
        self.button_compare.clicked.connect(self.compare_clos)
        self.progressbar = QProgressBar(self)

        action_layout.addWidget(self.button_compare)
        action_layout.addWidget(self.progressbar)
        main_layout.addLayout(action_layout)

        # Tabs for results
        self.tabs = QTabWidget()
        self.result_tab = QTextEdit()
        self.match_tab = QTextEdit()
        self.no_match_tab = QTextEdit()

        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        main_layout.addWidget(self.tabs)

        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def compare_clos(self):
        existing_file = self.entry_existing.text()
        new_file = self.entry_new.text()

        if not existing_file or not new_file:
            self.result_tab.setPlainText("Please select both files.")
            return

        # Extraction logic will now be handled in services
        from app.services.clo_extractor import extract_clos_from_file
        existing_clos = extract_clos_from_file(existing_file)
        new_clos = extract_clos_from_file(new_file)

        if not existing_clos or not new_clos:
            self.result_tab.setPlainText("No valid CLOs found in the files.")
            return

        # Proceed with the comparison using threading
        batch_size = 5
        batches = [list(existing_clos.items())[i:i + batch_size] for i in range(0, len(existing_clos), batch_size)]

        self.thread = CLOComparisonThread(existing_clos, new_clos, batches)
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
