from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from gui.Window import Window
from gui.EventManager import EventManager
from managers.user_manager import User
from managers.group_manager import Group


class AddUser(Window):
    def __init__(self, app):
        super().__init__(app)

    def compare_window(self, param: dict):
        return False

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
        group_label = QLabel("group")
        group_label.setFixedWidth(60)
        mail_label = QLabel("email")
        mail_label.setFixedWidth(60)

        self.name_edit = QLineEdit()
        self.surname_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.mail_edit = QLineEdit()
        self.group_combo_box = QComboBox()


        items = []
        for item in Group.get_list(12345, 1):
            if item.name == "Deleted":
                continue
            items.append(item.name)
        self.group_combo_box.addItems(items)

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

        mail_layout = QHBoxLayout()
        mail_layout.addWidget(mail_label)
        mail_layout.addWidget(self.mail_edit)

        group_layout = QHBoxLayout()
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo_box)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(add_button)

        vbox.addLayout(name_layout)
        vbox.addLayout(surname_layout)
        vbox.addLayout(address_layout)
        vbox.addLayout(phone_layout)
        vbox.addLayout(mail_layout)
        vbox.addLayout(group_layout)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add user")

        self.show()

    def add_user(self):
        dic = dict()
        dic["name"] = self.name_edit.text()
        dic["surname"] = self.surname_edit.text()
        dic["address"] = self.address_edit.text()
        dic["phone"] = int(self.phone_edit.text())
        dic["email"] = self.mail_edit.text()
        dic["group"] = Group.get(Group.name == self.group_combo_box.currentText())

        User.add(dic)
        self.app.el.fire(EventManager.Events.user_added, {})
        self.close()
