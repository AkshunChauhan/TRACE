# HelpTab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class HelpTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        help_text = QLabel("Help Information goes here.")
        layout.addWidget(help_text)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def close(self):
        self.setVisible(False)  # You can implement a different close behavior as needed
