from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QGroupBox, QPushButton, QFileDialog
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
        
        # Download Buttons
        self.download_all_button = QPushButton("Download All Results")
        self.download_overall_button = QPushButton("Download Overall Results")
        self.download_matching_button = QPushButton("Download Matching Courses")
        self.download_no_match_button = QPushButton("Download No Match Courses")
        
        self.download_all_button.clicked.connect(self.download_all_results)
        self.download_overall_button.clicked.connect(self.download_overall_results)
        self.download_matching_button.clicked.connect(self.download_matching_courses)
        self.download_no_match_button.clicked.connect(self.download_no_match_courses)

        layout.addWidget(self.tabs)
        layout.addWidget(self.download_all_button)
        layout.addWidget(self.download_overall_button)
        layout.addWidget(self.download_matching_button)
        layout.addWidget(self.download_no_match_button)

        self.setLayout(layout)

    def display_results(self, results, similarity_threshold, avg_similarity_threshold):
        # Set column headers for the table
        self.result_tab.setColumnCount(2)
        self.result_tab.setHorizontalHeaderLabels(["Course Name", "Average Similarity"])

        self.match_tab.setColumnCount(3)
        self.match_tab.setHorizontalHeaderLabels(["Course Name", "Existing CLO", "New CLO", "Similarity Score"])

        self.no_match_tab.setColumnCount(1)
        self.no_match_tab.setHorizontalHeaderLabels(["Course Name"])

        # Prepare rows
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

    def download_table(self, table_widget):
        # Get the number of rows and columns in the table
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

    def download_all_results(self):
        # Combine all tables into one and export
        all_data = []

        # Collect Overall Results
        rows = self.result_tab.rowCount()
        for row in range(rows):
            sheet_name = self.result_tab.item(row, 0).text()
            avg_similarity = self.result_tab.item(row, 1).text()
            all_data.append([sheet_name, avg_similarity])

        # Collect Matching Courses
        rows = self.match_tab.rowCount()
        for row in range(rows):
            sheet_name = self.match_tab.item(row, 0).text()
            existing_clo = self.match_tab.item(row, 1).text()
            new_clo = self.match_tab.item(row, 2).text()
            similarity_score = self.match_tab.item(row, 3).text()
            all_data.append([sheet_name, existing_clo, new_clo, similarity_score])

        # Collect No Match Courses
        rows = self.no_match_tab.rowCount()
        for row in range(rows):
            sheet_name = self.no_match_tab.item(row, 0).text()
            all_data.append([sheet_name])

        # Open file dialog to save combined results
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Combined Results", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)

        if file_name:
            # Save as CSV or Excel based on file extension
            if file_name.endswith(".csv"):
                df = pd.DataFrame(all_data)
                df.to_csv(file_name, index=False, header=False)
            elif file_name.endswith(".xlsx"):
                df = pd.DataFrame(all_data)
                df.to_excel(file_name, index=False, header=False)

    def download_overall_results(self):
        self.download_table(self.result_tab)

    def download_matching_courses(self):
        self.download_table(self.match_tab)

    def download_no_match_courses(self):
        self.download_table(self.no_match_tab)
