from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog, QMessageBox
from managers.user_manager import *


class AddUser(QWidget):
    def __init__(self):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_user)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(add_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add user")

    def add_user(self):
        print("add user")