import sys
from PyQt5.QtWidgets import QApplication
from ui_components import CLOComparisonApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CLOComparisonApp()
    window.show()
    sys.exit(app.exec_())
