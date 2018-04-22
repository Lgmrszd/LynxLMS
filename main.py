import sys

from PyQt5.QtWidgets import QStyleFactory, QApplication

from gui.Authorisation import Authorization
import db_config
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s \
    | %(levelname)s: %(message)s ') #logging config description
    db_config.init_db()
    # managers.user_manager.Queue.update_queue()

    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    auth = Authorization()
    auth.show()

    sys.exit(app.exec_())  # will not end until you close the program
