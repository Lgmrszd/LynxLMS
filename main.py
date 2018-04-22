import sys
import datetime

from PyQt5.QtWidgets import QStyleFactory, QApplication

from gui.Authorisation import Authorization
from managers import task_manager
import db_config
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s \
    | %(levelname)s: %(message)s ') #logging config description
    db_config.init_db()

    task_manager.Task.create(
        datetime=datetime.datetime.now(),
        func_name="update_queue",
        display_name="Update queue",
        parameters=[True])

    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    auth = Authorization()
    auth.show()

    sys.exit(app.exec_())  # will not end until you close the program
