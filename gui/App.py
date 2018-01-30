import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.MainWindow import MainWindow

class App:
    def __init__(self):
        app = QApplication(sys.argv)
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        main_window = MainWindow()
        main_window.show()

        sys.exit(app.exec_())#will not end until you close the program