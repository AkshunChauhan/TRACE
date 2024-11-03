from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal

class FileSelectionWidget(QWidget):
    update_files_signal = pyqtSignal(str, str)  # Signal that emits two string parameters

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.entry_existing = QLineEdit(self)
        self.entry_new = QLineEdit(self)
        self.button_select_existing = QPushButton("Select Existing File", self)
        self.button_select_new = QPushButton("Select New File", self)

        # Create layout for existing and new file selection
        file_selection_layout = QHBoxLayout()
        file_selection_layout.addWidget(self.entry_existing)
        file_selection_layout.addWidget(self.button_select_existing)
        file_selection_layout.addWidget(self.entry_new)
        file_selection_layout.addWidget(self.button_select_new)

        # Create main layout
        layout = QVBoxLayout(self)
        layout.addLayout(file_selection_layout)  # Add the horizontal layout
        self.setLayout(layout)

        # Connect button signals
        self.button_select_existing.clicked.connect(lambda: self.select_file('existing'))
        self.button_select_new.clicked.connect(lambda: self.select_file('new'))

    def select_file(self, file_type):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_type == 'existing':
            self.entry_existing.setText(file_path)
            self.update_files_signal.emit(file_path, self.entry_new.text())
        else:
            self.entry_new.setText(file_path)
            self.update_files_signal.emit(self.entry_existing.text(), file_path)
