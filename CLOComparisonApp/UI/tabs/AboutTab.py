# AboutTab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class AboutTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        about_text = QLabel("About Information goes here.")
        layout.addWidget(about_text)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def close(self):
        self.setVisible(False)  # Adjust the close behavior as needed
