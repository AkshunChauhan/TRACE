# In UI/tabs/SettingsTab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from UI.FileSelectionWidget import FileSelectionWidget
from UI.ThresholdWidget import ThresholdWidget

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Define file_selection_widget and threshold_widget as instance attributes
        self.file_selection_widget = FileSelectionWidget(self)
        self.threshold_widget = ThresholdWidget(self)

        layout.addWidget(self.file_selection_widget)
        layout.addWidget(self.threshold_widget)
        self.setLayout(layout)
