# FileTab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

class FileTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Dropdown for selecting files
        file_combo = QComboBox(self)
        file_combo.addItem("Select a file...")
        file_combo.addItem("File 1")
        file_combo.addItem("File 2")
        # Add more items as needed
        file_combo.setEditable(True)

        layout.addWidget(QLabel("Choose a file:"))
        layout.addWidget(file_combo)
        self.setLayout(layout)
