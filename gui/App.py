from gui.MainWindow import MainWindow
from gui.EventManager import EventManager


class App:
    def __init__(self, bs):
        self.bs = bs
        self.el = EventManager()
        self.windows = dict()

        self.open_window(MainWindow, {})

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
