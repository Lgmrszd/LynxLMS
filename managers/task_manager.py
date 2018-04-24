import datetime
import json
import peewee as pw
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from managers import event_manager
from db_connect import BaseModel

WAITING = 0
RUNNING = 1
ERROR = 2
FINISHED = 3

_tasks_functions = {}
_EM = None


class Task(BaseModel):
    """Task class which is used in task manager
    """
    task_id = pw.PrimaryKeyField()
    datetime = pw.DateTimeField()
    func_name = pw.CharField()
    display_name = pw.CharField()
    status = pw.SmallIntegerField(default=WAITING)
    args = pw.CharField()
    important = pw.BooleanField(default=False)
    message = pw.CharField(default="")

    @classmethod
    def create(cls, **query):
        # replace python list with its json representation
        if query.get("parameters"):
            query["args"] = json.dumps(query["parameters"])
        return super().create(**query)

    def get_id(self):
        """
        Returns task id
        :return: task id
        """
        return self.task_id

    def get_arguments(self):
        """
        Decode arguments from json
        :return: arguments to pass in function
        """
        return json.loads(self.args)

    def run(self):
        """
        Run task function
        :return: status as number and message as string
        """
        # Save status about current task
        self.status = RUNNING
        self.save()
        event_manager.send_event(f"task_started", self.display_name)
        # Send event signal about task with its info
        func = _tasks_functions[self.func_name]  # Get function by name
        # Try to execute task function normally and collect info about it (even if it fails)
        try:
            status, message = func(self.get_id(), self.get_arguments())
        except Exception as ex:
            status, message = ERROR, str(ex)
        # Save status about current task
        self.status = status
        self.message = message
        self.save()
        # Send event signal about task with its execution result
        event_manager.send_event(f"task_ended", status, message)
        # return execution result
        return status, message


def register_task_function(name, func):
    """
    Register task function by it's name
    task function should take two params: task_id (number) and parameters (list)
    task function should return two values: status (number, equal to WAITING, ERROR or FINISHED) and message (text)
    :param name: function name to register by
    :param func: python function or callable described above
    :return: None
    """
    _tasks_functions[name] = func


def inform_completeness(percentage):
    """
    Send signal to notify about task completeness
    :param percentage: number (0..100) representing task completeness
    :return: None
    """
    # Send event signal
    event_manager.send_event(f"task_completeness", percentage)


def get_tasks():
    """
    Get all tasks
    :return: tasks list
    """
    tasks = list(Task.select().order_by(Task.datetime.asc))
    return tasks


def run_task(task_id):
    """
    Run task by it's id
    :param task_id: id of task to be run
    :return: status as number and message as string
    """
    task = Task.get(Task.task_id == task_id)
    return task.run()


def timer_function():
    """
    Checks if there are any task to run
    :return: None
    """
    now = datetime.datetime.now()
    # Get waiting tasks and run them
    auto_tasks = Task.select().where(Task.datetime < now).\
        where(Task.status == WAITING).order_by(Task.datetime.asc())
    for task in auto_tasks:
        task.run()

    # Get error tasks and delete them
    old = now - datetime.timedelta(weeks=1)
    error_tasks = Task.select().where(Task.datetime < old).\
        where(Task.status == ERROR).order_by(Task.datetime.asc())
    for task in error_tasks:
        task.delete_instance()
    error_tasks = Task.select().where(Task.datetime < old).\
        where(Task.status == RUNNING).order_by(Task.datetime.asc())
    for task in error_tasks:
        task.delete_instance()

    # Get finished tasks and delete them
    old = now - datetime.timedelta(weeks=1)
    error_tasks = Task.select().where(Task.datetime < old).\
        where(Task.status == FINISHED).order_by(Task.datetime.asc())
    for task in error_tasks:
        task.delete_instance()


def tick():
    if _EM:
        timer_function()


def add_EventManager(EM):
    global _EM
    _EM = EM


class TimerThread(QThread):
    __startSignal = pyqtSignal(str)
    __updateSignal = pyqtSignal(int)
    __endSignal = pyqtSignal(int, str)

    def __init__(self, start_slot, update_slot, end_slot):
        super().__init__()
        self.__startSignal.connect(start_slot)
        self.__updateSignal.connect(update_slot)
        self.__endSignal.connect(end_slot)
        event_manager.register_listener("task_started", self.start_signal)
        event_manager.register_listener("task_completeness", self.update_signal)
        event_manager.register_listener("task_ended", self.end_signal)
        # self.updateSignal.connect()
        # self.started.connect(lambda: )

    def start_signal(self, display_name):
        self.__startSignal.emit(display_name)

    def update_signal(self, percentage):
        self.__updateSignal.emit(percentage)

    def end_signal(self, status, message):
        self.__endSignal.emit(status, message)

    def run(self):
        print("startKek")
        timer = QTimer()
        timer.timeout.connect(timer_function)
        timer.start(1000)
        self.exec_()
