from PyQt5.QtWidgets import QFileDialog

def select_file(parent, file_type, entry_field):
    """Helper function to open a file dialog and select an Excel file."""
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(parent, f"Select {file_type.capitalize()} Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
    if file_name:
        entry_field.setText(file_name)
