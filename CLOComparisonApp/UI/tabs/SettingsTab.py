from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from UI.FileSelectionWidget import FileSelectionWidget
from UI.ThresholdWidget import ThresholdWidget


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # File selection and threshold widgets
        self.file_selection_widget = FileSelectionWidget(self)
        self.threshold_widget = ThresholdWidget(self)

        # Create a table for displaying results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Sheet Name", "Average Similarity (%)"])
        
        # Adjust column sizes dynamically
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.results_table.horizontalHeader().setStretchLastSection(True)

        # Use a splitter to divide the left and right sides
        splitter = QSplitter()
        left_side = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.file_selection_widget)
        left_layout.addWidget(self.threshold_widget)
        left_side.setLayout(left_layout)
        splitter.addWidget(left_side)
        splitter.addWidget(self.results_table)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def update_results(self, results):
        """Update the table with results."""
        self.results_table.setRowCount(len(results))
        for row, (sheet_name, average_similarity) in enumerate(results):
            # Format average similarity as percentage
            percentage_similarity = average_similarity * 100  # Convert to percentage
            self.results_table.setItem(row, 0, QTableWidgetItem(sheet_name))
            self.results_table.setItem(row, 1, QTableWidgetItem(f"{percentage_similarity:.2f}%"))

        # Resize columns to fit content dynamically
        self.results_table.resizeColumnsToContents()
