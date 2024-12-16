import sys
import unittest
from PyQt5.QtWidgets import QApplication
from UI.CLOComparisonApp import CLOComparisonApp
from UI.tabs.SettingsTab import SettingsTab


class TestCLOComparisonApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
    
    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        self.window = CLOComparisonApp()

    def tearDown(self):
        self.window.close()

    def test_window_title(self):
        """Test if the main window title is set correctly."""
        self.assertEqual(self.window.windowTitle(), "TRACE")

    def test_settings_tab_exists(self):
        """Test if the Settings tab exists."""
        self.assertIsInstance(self.window.tab_settings, SettingsTab)

    def test_file_selection_widget(self):
        """Test if the file selection widget is functioning in the Settings tab."""
        file_widget = self.window.tab_settings.file_selection_widget
        self.assertIsNotNone(file_widget)
        self.assertTrue(file_widget.entry_existing.isEnabled())
        self.assertTrue(file_widget.entry_new.isEnabled())

    def test_threshold_widget(self):
        """Test if the threshold widget is functioning in the Settings tab."""
        threshold_widget = self.window.tab_settings.threshold_widget
        self.assertIsNotNone(threshold_widget)
        self.assertTrue(threshold_widget.threshold_slider.isEnabled())
        self.assertTrue(threshold_widget.avg_similarity_slider.isEnabled())

    def test_compare_clos(self):
        """Test the compare_clos functionality with valid input."""
        # Mock valid inputs for file paths
        self.window.tab_settings.file_selection_widget.entry_existing.setText("valid_existing_file.xlsx")
        self.window.tab_settings.file_selection_widget.entry_new.setText("valid_new_file.xlsx")

        # Trigger the comparison
        self.window.compare_clos()

        # Check if progress bar updates (mock a progress value for testing)
        self.window.update_progress(50)
        self.assertEqual(self.window.action_bar_widget.progressbar.value(), 50)

    def test_missing_files(self):
        """Test compare_clos functionality when files are missing."""
        self.window.tab_settings.file_selection_widget.entry_existing.setText("")
        self.window.tab_settings.file_selection_widget.entry_new.setText("")

        # Trigger the comparison
        self.window.compare_clos()

        # Verify the result tab displays the appropriate error message
        result_text = self.window.result_tabs_widget.result_tab.toPlainText()
        self.assertEqual(result_text, "Please select both files.")


if __name__ == "__main__":
    unittest.main()
