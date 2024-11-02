from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QSlider,
    QVBoxLayout,
)


def create_file_selection_group(parent):
    file_selection_group = QGroupBox("Step 1: Select Files")
    file_selection_layout = QHBoxLayout()

    # Existing File Section
    existing_file_layout = QFormLayout()
    entry_existing = QLineEdit(parent)
    button_existing = QPushButton("Browse", parent)
    button_existing.clicked.connect(lambda: parent.select_file("existing"))
    existing_file_layout.addRow(QLabel("Existing Excel File:"), entry_existing)
    existing_file_layout.addRow("", button_existing)

    # New File Section
    new_file_layout = QFormLayout()
    entry_new = QLineEdit(parent)
    button_new = QPushButton("Browse", parent)
    button_new.clicked.connect(lambda: parent.select_file("new"))
    new_file_layout.addRow(QLabel("New Excel File:"), entry_new)
    new_file_layout.addRow("", button_new)

    # Add layouts to the horizontal layout
    file_selection_layout.addLayout(existing_file_layout)
    file_selection_layout.addLayout(new_file_layout)
    file_selection_group.setLayout(file_selection_layout)

    return entry_existing, entry_new, file_selection_group


def create_threshold_group(parent):
    threshold_group = QGroupBox("Step 2 & 3: Set Similarity Thresholds")
    threshold_layout = QHBoxLayout()

    # Similarity Threshold Slider
    similarity_layout = QVBoxLayout()
    threshold_label = QLabel("Similarity Threshold: 0.5", parent)
    threshold_slider = QSlider(Qt.Horizontal)
    threshold_slider.setRange(0, 100)
    threshold_slider.setValue(50)
    threshold_slider.valueChanged.connect(
        lambda: update_label(threshold_slider, threshold_label, "Similarity Threshold")
    )
    similarity_layout.addWidget(threshold_label)
    similarity_layout.addWidget(threshold_slider)

    # Average Similarity Threshold Slider
    avg_similarity_layout = QVBoxLayout()
    avg_similarity_label = QLabel("Average Similarity Threshold: 0.5", parent)
    avg_similarity_slider = QSlider(Qt.Horizontal)
    avg_similarity_slider.setRange(0, 100)
    avg_similarity_slider.setValue(50)
    avg_similarity_slider.valueChanged.connect(
        lambda: update_label(
            avg_similarity_slider, avg_similarity_label, "Average Similarity Threshold"
        )
    )
    avg_similarity_layout.addWidget(avg_similarity_label)
    avg_similarity_layout.addWidget(avg_similarity_slider)

    # Add both sliders to the threshold layout side-by-side
    threshold_layout.addLayout(similarity_layout)
    threshold_layout.addLayout(avg_similarity_layout)
    threshold_group.setLayout(threshold_layout)

    return threshold_slider, avg_similarity_slider, threshold_group
