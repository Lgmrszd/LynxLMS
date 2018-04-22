import datetime
import json
import peewee as pw
from managers import event_manager
from db_connect import BaseModel

WAITING = 0
RUNNING = 1
ERROR = 2
FINISHED = 3

_tasks_functions = {}


class Task(BaseModel):
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
        if query.get("parameters"):
            query["args"] = json.dumps(query["parameters"])
        return super().create(**query)

    def get_id(self):
        return self.task_id

    def get_arguments(self):
        return json.loads(self.args)

    def run(self):
        self.status = RUNNING
        self.save()
        func = _tasks_functions[self.func_name]
        try:
            status, message = func(self.get_id(), self.get_arguments())
        except Exception as ex:
            status, message = ERROR, str(ex)
        self.status = status
        self.message = message
        self.save()
        return status, message


def register_task_function(name, func):
    _tasks_functions[name] = func


def inform_completeness(percentage):
    event_manager.send_event(f"task_completeness", percentage)


def get_tasks():
    return Task.select().order_by(Task.datetime.asc)


def timer_function():
    now = datetime.datetime.now()
    auto_tasks = Task.select().where(Task.datetime < now).\
        where(Task.status == WAITING).\
        where(Task.important is not False).order_by(Task.datetime.asc())
    for task in auto_tasks:
        task.run()
