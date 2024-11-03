# ResultTabsWidget.py
from PyQt5.QtWidgets import QTabWidget, QTextEdit, QVBoxLayout, QGroupBox

class ResultTabsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Results", parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.result_tab = QTextEdit()
        self.match_tab = QTextEdit()
        self.no_match_tab = QTextEdit()
        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def display_results(self, results, similarity_threshold, avg_similarity_threshold):
        overall_result_text = ""
        match_result_text = ""
        no_match_result_text = ""

        for sheet_name, average_similarity, highest_similarity_pairs in results:
            overall_result_text += (
                f"Course: {sheet_name}, Average Similarity: {average_similarity:.2f}\n"
            )
            if average_similarity >= similarity_threshold:  # Use dynamic threshold
                match_result_text += f"\nMatching Course: {sheet_name}\n"
                for existing_clo, new_clo, score in highest_similarity_pairs:
                    match_result_text += (
                        f"  Existing CLO: {existing_clo}\n  New CLO: {new_clo}\n  Similarity Score: {score:.2f}\n"
                    )
            else:
                no_match_result_text += f"No match found for course: {sheet_name}\n"

        self.result_tab.setPlainText(overall_result_text)
        self.match_tab.setPlainText(match_result_text)
        self.no_match_tab.setPlainText(no_match_result_text)
