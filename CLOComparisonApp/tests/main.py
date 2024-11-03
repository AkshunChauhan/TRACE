import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtAxContainer import QAxWidget


class ExcelEmbed(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.axWidget = QAxWidget()
        self.layout.addWidget(self.axWidget)

        self.axWidget.setControl(
            "{00020813-0000-0000-C000-000000000046}"
        )  # Excel Application

        self.setWindowTitle("Excel Embed")
        self.show()

        self.browseButton = QPushButton("Browse Excel File", self)
        self.layout.addWidget(self.browseButton)
        self.browseButton.clicked.connect(self.browseExcelFile)

    def browseExcelFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xls *.xlsx)"
        )

        if filePath:
            self.axWidget.dynamicCall("Workbooks.Open(FileName='{}')".format(filePath))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    excelEmbed = ExcelEmbed()
    sys.exit(app.exec_())
