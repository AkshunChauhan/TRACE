import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from UI.CLOComparisonApp import CLOComparisonApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('TRACE\\CLOComparisonApp\\icons\\Logo.jpg'))
    window = CLOComparisonApp()
    window.show()
    sys.exit(app.exec_())
