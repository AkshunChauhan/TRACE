from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)
from PyQt5.QtCore import pyqtSignal


class FileSelectionWidget(QWidget):
    update_files_signal = pyqtSignal(str, str)  # Signal that emits two string parameters

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Widgets for existing file selection
        self.label_existing = QLabel("Choose Existing File:")
        self.entry_existing = QLineEdit(self)
        self.button_select_existing = QPushButton("Browse", self)

        # Layout for existing file selection
        existing_layout = QHBoxLayout()
        existing_layout.addWidget(self.entry_existing)
        existing_layout.addWidget(self.button_select_existing)

        # Widgets for new file selection
        self.label_new = QLabel("Choose New File:")
        self.entry_new = QLineEdit(self)
        self.button_select_new = QPushButton("Browse", self)

        # Layout for new file selection
        new_layout = QHBoxLayout()
        new_layout.addWidget(self.entry_new)
        new_layout.addWidget(self.button_select_new)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_existing)  # Add label for existing file
        layout.addLayout(existing_layout)  # Add input and button for existing file
        layout.addWidget(self.label_new)  # Add label for new file
        layout.addLayout(new_layout)  # Add input and button for new file
        self.setLayout(layout)

        # Connect button signals
        self.button_select_existing.clicked.connect(lambda: self.select_file("existing"))
        self.button_select_new.clicked.connect(lambda: self.select_file("new"))

    def select_file(self, file_type):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_type == "existing":
            self.entry_existing.setText(file_path)
            self.update_files_signal.emit(file_path, self.entry_new.text())
        else:
            self.entry_new.setText(file_path)
            self.update_files_signal.emit(self.entry_existing.text(), file_path)
