import datetime

from gui.MainWindow import MainWindow
from gui.EventManager import EventManager
from managers import task_manager
from managers.task_manager import TimerThread


class App:
    el = None

    def __init__(self, bs):
        self.bs = bs
        App.el = EventManager()
        self.windows = dict()

        self.open_window(MainWindow, {})

        task_manager.Task.create(
            datetime=datetime.datetime.now(),
            func_name="update_queue",
            display_name="Update queue",
            parameters=[True])

        tt = TimerThread(App.start_slot, App.update_slot, App.end_slot)
        tt.start()

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

    @classmethod
    def start_slot(cls, display_name):
        if App.el:
            App.el.fire(EventManager.Events.task_started, {"name": display_name})

    @classmethod
    def update_slot(cls, percentage):
        if App.el:
            App.el.fire(EventManager.Events.task_completeness, {"progress": percentage})

    @classmethod
    def end_slot(cls, status, message):
        if App.el:
            if status == 2:
                App.el.fire(EventManager.Events.task_crashed, {"message": message})
            elif status == 3:
                App.el.fire(EventManager.Events.task_finished, {"message": message})
