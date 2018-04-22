import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.MainWindow import MainWindow
from gui.EventManager import EventManager


class App:
    def __init__(self):
        self.el = EventManager()
        self.windows = dict()

        app = QApplication(sys.argv)
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.open_window(MainWindow, {})

        sys.exit(app.exec_())  # will not end until you close the program

    def open_window(self, cls, param):
        if self.windows.get(cls) is None:
            self.windows[cls] = list()
        for i in self.windows[cls]:
            if i.compare_window(param):
                i.show()
                i.activateWindow()
                return None
        win = cls(self, **param)
        self.windows[cls].append(win)
        return win

    def forget_window(self, window) -> None:
        self.windows[type(window)].remove(window)
        self.el.delete_all(window)
