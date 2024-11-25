from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QGroupBox, QPushButton, QFileDialog, QDialog, QRadioButton, QDialogButtonBox
import pandas as pd

class ResultTabsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Results", parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Initialize QTableWidget for each tab
        self.result_tab = QTableWidget()
        self.match_tab = QTableWidget()
        self.no_match_tab = QTableWidget()

        # Add tabs
        self.tabs.addTab(self.result_tab, "Overall Results")
        self.tabs.addTab(self.match_tab, "Matching Courses")
        self.tabs.addTab(self.no_match_tab, "No Match Courses")
        
        # Download Button
        self.download_button = QPushButton("Download Results")
        self.download_button.clicked.connect(self.show_download_dialog)

        layout.addWidget(self.tabs)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def display_results(self, results, similarity_threshold, avg_similarity_threshold):
        """Populate the tables with results."""
        # Set column headers for the tables
        self.result_tab.setColumnCount(2)
        self.result_tab.setHorizontalHeaderLabels(["Course Name", "Average Similarity"])

        self.match_tab.setColumnCount(3)
        self.match_tab.setHorizontalHeaderLabels(["Course Name", "Existing CLO", "New CLO", "Similarity Score"])

        self.no_match_tab.setColumnCount(1)
        self.no_match_tab.setHorizontalHeaderLabels(["Course Name"])

        # Prepare rows for each table
        self.result_tab.setRowCount(len(results))
        self.match_tab.setRowCount(0)  # We'll add rows dynamically
        self.no_match_tab.setRowCount(0)

        row_index = 0
        for sheet_name, average_similarity, highest_similarity_pairs in results:
            # Populate the overall result table with decimal similarity
            self.result_tab.setItem(row_index, 0, QTableWidgetItem(sheet_name))
            self.result_tab.setItem(row_index, 1, QTableWidgetItem(f"{average_similarity:.2f}"))
            row_index += 1

            # Check if the course meets the similarity threshold
            if average_similarity >= similarity_threshold:
                for existing_clo, new_clo, score in highest_similarity_pairs:
                    row_position = self.match_tab.rowCount()
                    self.match_tab.insertRow(row_position)
                    self.match_tab.setItem(row_position, 0, QTableWidgetItem(sheet_name))
                    self.match_tab.setItem(row_position, 1, QTableWidgetItem(existing_clo))
                    self.match_tab.setItem(row_position, 2, QTableWidgetItem(new_clo))
                    self.match_tab.setItem(row_position, 3, QTableWidgetItem(f"{score * 100:.2f}%"))
            else:
                row_position = self.no_match_tab.rowCount()
                self.no_match_tab.insertRow(row_position)
                self.no_match_tab.setItem(row_position, 0, QTableWidgetItem(sheet_name))

        # Resize columns to fit content
        self.result_tab.resizeColumnsToContents()
        self.match_tab.resizeColumnsToContents()
        self.no_match_tab.resizeColumnsToContents()

    def show_download_dialog(self):
        """Open a dialog to choose which data to download."""
        dialog = DownloadChoiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get selected choice and trigger download
            download_choice = dialog.get_download_choice()
            if download_choice == 'overall':
                self.download_table(self.result_tab)
            elif download_choice == 'matching':
                self.download_table(self.match_tab)
            elif download_choice == 'no_match':
                self.download_table(self.no_match_tab)

    def download_table(self, table_widget):
        """Download the selected table as a CSV or Excel file."""
        rows = table_widget.rowCount()
        columns = table_widget.columnCount()

        # Prepare data to write to a CSV or Excel file
        data = []
        for row in range(rows):
            row_data = []
            for col in range(columns):
                item = table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Open a file dialog to save the file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        
        if file_name:
            # Save as CSV or Excel based on file extension
            if file_name.endswith(".csv"):
                df = pd.DataFrame(data)
                df.to_csv(file_name, index=False, header=False)
            elif file_name.endswith(".xlsx"):
                df = pd.DataFrame(data)
                df.to_excel(file_name, index=False, header=False)


class DownloadChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Data to Download")
        layout = QVBoxLayout()

        # Radio buttons for different download options
        self.overall_button = QRadioButton("Overall Results")
        self.matching_button = QRadioButton("Matching Courses")
        self.no_match_button = QRadioButton("No Match Courses")

        # Set default selection
        self.overall_button.setChecked(True)

        layout.addWidget(self.overall_button)
        layout.addWidget(self.matching_button)
        layout.addWidget(self.no_match_button)

        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_download_choice(self):
        """Return the selected download option."""
        if self.overall_button.isChecked():
            return 'overall'
        elif self.matching_button.isChecked():
            return 'matching'
        elif self.no_match_button.isChecked():
            return 'no_match'
