import datetime
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QStyleFactory, QApplication

from gui.Authorisation import Authorization
import db_config
import logging
from managers import task_manager

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s \
    | %(levelname)s: %(message)s ') #logging config description
    db_config.init_db()

    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    auth = Authorization()
    auth.show()

    task_manager.Task.create(
        datetime=datetime.datetime.now(),
        func_name="update_queue",
        display_name="Update queue",
        parameters=[True])

    t = QTimer()
    t.timeout.connect(task_manager.tick)
    t.setInterval(1000)
    t.start()

    sys.exit(app.exec_())  # will not end until you close the program
