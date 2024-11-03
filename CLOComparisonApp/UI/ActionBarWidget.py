# ActionBarWidget.py
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QProgressBar, QWidget

class ActionBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        
        self.button_compare = QPushButton("Compare CLOs", self)
        layout.addWidget(self.button_compare)

        self.progressbar = QProgressBar(self)
        layout.addWidget(self.progressbar)

        self.setLayout(layout)

    def update_file_paths(self, existing_path, new_path):
        # Logic to handle file paths
        print(f"Existing file path: {existing_path}")
        print(f"New file path: {new_path}")
