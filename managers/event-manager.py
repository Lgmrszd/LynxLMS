import peewee as pw
from PyQt5.QtCore import QTimer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber
from db_connect import BaseModel
import time


class Event(BaseModel):
    event_id = pw.PrimaryKeyField()
    datetime = pw.DateTimeField()
    event_name = pw.CharField()


class _EventManager:
    def __init__(self):
        self._listeners = {}

    def register_listener(self, name, func):
        listeners = self._listeners.get(name, None)
        if listeners:
            self._listeners[name].append(func)
        else:
            self._listeners[name] = [func]

    def send_event(self, name, *args):
        listeners = self._listeners.get(name, None)
        if listeners:
            if args:
                for listener in listeners:
                    result = listener(*args)
            else:
                for listener in listeners:
                    result = listener()


EventManager = _EventManager()

# Test
# EventManager.register_listener("test", lambda: print("Hello World!"))
# EventManager.register_listener("test2", lambda x: print("Hello, "+x))
# EventManager.send_event("test")
# EventManager.send_event("test2", "Anton")


def test():
    print("test 1 start")
    time.sleep(5)
    print("test 1 end")


def test2():
    print("test 2 start")
    time.sleep(5)
    print("test 2 end")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')

    btn = QPushButton('Button', w)
    btn.resize(btn.sizeHint())
    btn.move(0, 50)
    print(btn.clicked, type(btn.clicked))

    timer = QTimer()
    # timer.tim

    btn.clicked.connect(test)

    w.show()

    sys.exit(app.exec_())
