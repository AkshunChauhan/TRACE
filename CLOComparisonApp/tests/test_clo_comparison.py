import sys
import os
import unittest  # This was missing

# Add the root project directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from UI.CLOComparisonApp import CLOComparisonApp

class TestCLOComparisonApp(unittest.TestCase):
    def test_compare_clos(self):
        app = CLOComparisonApp()

        # Simulate user input and file paths here
        app.settings_tab.file_selection_widget.entry_existing.setText("path/to/existing_file.xlsx")
        app.settings_tab.file_selection_widget.entry_new.setText("path/to/new_file.xlsx")

        # Trigger the compare function
        app.compare_clos()

        # Check if result tabs or error message gets updated accordingly
        self.assertTrue("comparison results" in app.result_tabs_widget.result_tab.toPlainText())

if __name__ == '__main__':
    unittest.main()
