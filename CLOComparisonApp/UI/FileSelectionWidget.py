from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFileDialog,
    QSizePolicy,
    QMessageBox,  # Add QMessageBox for user feedback
)
from PyQt5.QtCore import pyqtSignal
import os

import pandas as pd  # Add this import for validating Excel files

class FileSelectionWidget(QWidget):
    update_files_signal = pyqtSignal(str, str)  # Signal that emits two string parameters

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Step 1: Label and Box
        self.step_box = QGroupBox("Step 1: File Selection", self)
        step_box_layout = QVBoxLayout()

        # Widgets for existing file selection inside Step 1 box
        self.label_existing = QLabel("Choose Existing File:")
        self.entry_existing = QLineEdit(self)
        self.button_select_existing = QPushButton("Browse", self)

        # Layout for existing file selection
        existing_layout = QHBoxLayout()
        existing_layout.addWidget(self.entry_existing)
        existing_layout.addWidget(self.button_select_existing)

        # Widgets for new file selection inside Step 1 box
        self.label_new = QLabel("Choose New File:")
        self.entry_new = QLineEdit(self)
        self.button_select_new = QPushButton("Browse", self)

        # Layout for new file selection
        new_layout = QHBoxLayout()
        new_layout.addWidget(self.entry_new)
        new_layout.addWidget(self.button_select_new)

        # Add existing and new file selection layouts to the step box
        step_box_layout.addWidget(self.label_existing)
        step_box_layout.addLayout(existing_layout)
        step_box_layout.addWidget(self.label_new)
        step_box_layout.addLayout(new_layout)

        self.step_box.setLayout(step_box_layout)

        # Adjust size hint or size policy for consistent sizing
        self.step_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.step_box.setMinimumHeight(150)  # Ensure minimum height to match Step 2

        # Main layout for the widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.step_box)  # Add Step 1 box with file selection widgets
        self.setLayout(layout)

        # Connect button signals
        self.button_select_existing.clicked.connect(lambda: self.select_file("existing"))
        self.button_select_new.clicked.connect(lambda: self.select_file("new"))

    def select_file(self, file_type):
        try:
            # Show file dialog
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)"
            )

            if not file_path:
                # No file selected
                QMessageBox.warning(self, "No File Selected", "Please select a valid file.")
                return

            # Check if the file exists and is readable
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Invalid File", "The selected file does not exist.")
                return

            # Validate file content
            if not self.validate_file(file_path):
                QMessageBox.critical(self, "Invalid Data", "The selected file doesn't contain enough data.")
                return

            if file_type == "existing":
                self.entry_existing.setText(file_path)
                self.update_files_signal.emit(file_path, self.entry_new.text())
            else:
                self.entry_new.setText(file_path)
                self.update_files_signal.emit(self.entry_existing.text(), file_path)

        except Exception as e:
            # Catch unexpected errors and show a critical error message
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            print(f"Error selecting file: {e}")  # Optional: Log to console or a file

    def validate_file(self, file_path):
        """
        Validates if the selected Excel file contains enough data.
        """
        try:
            # Read the file using pandas
            df = pd.read_excel(file_path)

            # Check if the DataFrame is empty
            if df.empty or len(df.columns) < 2:
                return False

            # Check if there are enough rows for comparison
            if len(df) < 2:
                return False

            return True  # File is valid
        except Exception as e:
            print(f"Error validating file: {e}")
            return False
