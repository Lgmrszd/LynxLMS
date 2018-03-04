from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog, QMessageBox
from managers.user_manager import User
from managers.group_manager import Group


class AddUser(QWidget):
    def __init__(self):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        name_label = QLabel("name")
        name_label.setFixedWidth(60)
        surname_label = QLabel("surname")
        surname_label.setFixedWidth(60)
        address_label = QLabel("address")
        address_label.setFixedWidth(60)
        phone_label = QLabel("phone")
        phone_label.setFixedWidth(60)

        self.name_edit = QLineEdit()
        self.surname_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.phone_edit = QLineEdit()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_user)

        vbox = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)

        surname_layout = QHBoxLayout()
        surname_layout.addWidget(surname_label)
        surname_layout.addWidget(self.surname_edit)

        address_layout = QHBoxLayout()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_edit)

        phone_layout = QHBoxLayout()
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_edit)

        group_layout = QHBoxLayout()

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(add_button)

        vbox.addLayout(name_layout)
        vbox.addLayout(surname_layout)
        vbox.addLayout(address_layout)
        vbox.addLayout(phone_layout)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add user")

    def add_user(self):
        group = Group.add(
            {
                "name":"Group",
                "book_ct":2,
                "book_bestseller_ct":1,
                "journal_ct":2,
                "av_ct":2
            }
        )

        dic = dict()
        dic["name"] = self.name_edit.text()
        dic["surname"] = self.surname_edit.text()
        dic["address"] = self.address_edit.text()
        dic["phone"] = int(self.phone_edit.text())
        dic["group"] = group

        User.add(dic)
        self.close()