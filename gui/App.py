import datetime

from PyQt5.QtCore import QTimer

from gui.MainWindow import MainWindow
from gui.EventManager import EventManager
from managers import task_manager


class App:
    def __init__(self, bs):
        self.bs = bs
        self.el = EventManager()
        self.windows = dict()

        task_manager.Task.create(
            datetime=datetime.datetime.now(),
            func_name="update_queue",
            display_name="Update queue",
            parameters=[True])

        t = QTimer()
        t.timeout.connect(task_manager.timer_function)
        t.start(1000)

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
