from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QProgressBar, QWidget, QMessageBox

class ActionBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        
        self.button_compare = QPushButton("Start Compare", self)
        self.button_compare.setEnabled(False)  # Initially disabled
        layout.addWidget(self.button_compare)

        self.progressbar = QProgressBar(self)
        layout.addWidget(self.progressbar)

        self.setLayout(layout)

    def update_file_paths(self, existing_path, new_path):
        # Handle file path updates
        print(f"Existing file path: {existing_path}")
        print(f"New file path: {new_path}")

        # Enable the button only if both file paths are provided
        if existing_path and new_path:
            self.button_compare.setEnabled(True)
        else:
            self.button_compare.setEnabled(False)
        
    def show_error_message(self, title, message):
        """Show a critical error message box."""
        QMessageBox.critical(self, title, message)
