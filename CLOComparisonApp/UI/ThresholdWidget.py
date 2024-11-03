# ThresholdWidget.py
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt  # Import Qt here

class ThresholdWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Step 2 & 3: Set Similarity Thresholds", parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Similarity Threshold Slider
        self.threshold_label = QLabel("Similarity Threshold: 0.5", self)
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 100)
        self.threshold_slider.setValue(50)
        self.threshold_slider.valueChanged.connect(self.update_threshold_label)

        similarity_layout = QVBoxLayout()
        similarity_layout.addWidget(self.threshold_label)
        similarity_layout.addWidget(self.threshold_slider)

        # Average Similarity Threshold Slider
        self.avg_similarity_label = QLabel("Average Similarity Threshold: 0.5", self)
        self.avg_similarity_slider = QSlider(Qt.Horizontal)
        self.avg_similarity_slider.setRange(0, 100)
        self.avg_similarity_slider.setValue(50)
        self.avg_similarity_slider.valueChanged.connect(self.update_avg_similarity_label)

        avg_similarity_layout = QVBoxLayout()
        avg_similarity_layout.addWidget(self.avg_similarity_label)
        avg_similarity_layout.addWidget(self.avg_similarity_slider)

        # Add both sliders to the threshold layout
        layout.addLayout(similarity_layout)
        layout.addLayout(avg_similarity_layout)
        self.setLayout(layout)

    def update_threshold_label(self):
        threshold_value = self.threshold_slider.value() / 100
        self.threshold_label.setText(f"Similarity Threshold: {threshold_value:.2f}")

    def update_avg_similarity_label(self):
        avg_similarity_value = self.avg_similarity_slider.value() / 100
        self.avg_similarity_label.setText(f"Average Similarity Threshold: {avg_similarity_value:.2f}")
