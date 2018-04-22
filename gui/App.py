import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.MainWindow import MainWindow
from gui.Authorisation import Authorization

class App:
    def __init__(self):
        app = QApplication(sys.argv)
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        auth = Authorization()
        auth.show()

        sys.exit(app.exec_())#will not end until you close the program