from db_connect import BaseModel
import peewee as pw
import time
import datetime
import json
from managers import event_manager

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

    def __init__(self, **kwargs):
        if kwargs.get("parameters"):
            kwargs["args"] = json.dumps(kwargs["parameters"])
        super().__init__(**kwargs)

    def get_id(self):
        return self.task_id

    def get_arguments(self):
        return json.loads(self.args)

    def run(self):
        func = _tasks_functions[self.func_name]
        status, message = func(self.get_id(), self.get_arguments())
        self.status = status
        self.save()
        return status, message


def register_task_function(name, func):
    _tasks_functions[name] = func


def inform_completeness(percentage):
    event_manager.send_event(f"task_completeness", percentage)


def get_tasks():
    return Task.select().order_by(Task.datetime.asc)
