import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui.main_window import CLOComparisonApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CLOComparisonApp()
    window.show()
    sys.exit(app.exec_())
