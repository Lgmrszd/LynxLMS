from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from gui.Window import Window
from gui.EventManager import EventManager
import os.path


class AdminPanel(Window):
    def __init__(self, app):
        super().__init__(app)

    def _set_up_ui(self):
        window_size_x = 1200
        window_size_y = 800

        vbox = QVBoxLayout()

        label = QLabel()
        pixmap = QPixmap(os.path.dirname(__file__) + '/../images/hacker.jpg').scaledToHeight(250).scaledToWidth(250)
        label.setPixmap(pixmap)

        logs_label = QLabel("<h1>Logs</h1>")

        logs = QTextEdit()
        logs.setReadOnly(True)

        full_log = ''

        f = open(os.path.dirname(__file__) + '/../main.log')

        for line in f.readlines():
            full_log += line

        f.close()
        logs.setText(full_log)

        logs_label_layout = QHBoxLayout()
        logs_label_layout.addWidget(logs_label)
        logs_label_layout.addStretch()

        hbox_pic = QHBoxLayout()
        hbox_pic.addStretch()
        hbox_pic.addWidget(label)

        vbox.addLayout(hbox_pic)
        vbox.addLayout(logs_label_layout)
        vbox.addWidget(logs)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Admin panel')