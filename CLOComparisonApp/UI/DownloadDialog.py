from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLabel, QFileDialog
import pandas as pd

class DownloadDialog(QDialog):
    def __init__(self, result_tabs_widget, parent=None):
        super().__init__(parent)
        self.result_tabs_widget = result_tabs_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label for the dialog
        self.label = QLabel("Select the results file to download:", self)
        layout.addWidget(self.label)

        # ComboBox to select which file to download
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Overall Results")
        self.combo_box.addItem("Matching Courses")
        self.combo_box.addItem("No Match Courses")
        self.combo_box.addItem("All Results Combined")
        layout.addWidget(self.combo_box)

        # Download Button
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_selected_results)
        layout.addWidget(self.download_button)

        self.setLayout(layout)
        self.setWindowTitle("Download Results")

    def download_selected_results(self):
        selected_option = self.combo_box.currentText()
        
        if selected_option == "Overall Results":
            self.result_tabs_widget.download_overall_results()
        elif selected_option == "Matching Courses":
            self.result_tabs_widget.download_matching_courses()
        elif selected_option == "No Match Courses":
            self.result_tabs_widget.download_no_match_courses()
        elif selected_option == "All Results Combined":
            self.result_tabs_widget.download_all_results()
        
        self.accept()  # Close the dialog after downloading
