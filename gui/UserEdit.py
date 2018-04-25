from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit

from gui.GUITools import add_button
from managers.user_manager import User
from gui.Window import Window
from gui.EventManager import EventManager


class UserEdit(Window):
    def __init__(self, app, user):
        self.user = user
        super().__init__(app)

    def compare_window(self, param: dict):
        return self.user.card_id == param["user"].card_id

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
        mail_label = QLabel("email")
        mail_label.setFixedWidth(60)

        self.name_edit = QLineEdit()
        self.name_edit.setText(self.user.name)
        self.surname_edit = QLineEdit()
        self.surname_edit.setText(self.user.surname)
        self.address_edit = QLineEdit()
        self.address_edit.setText(self.user.address)
        self.phone_edit = QLineEdit()
        self.phone_edit.setText(str(self.user.phone))
        self.mail_edit = QLineEdit()
        self.mail_edit.setText(str(self.user.email))

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

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button(add_button_layout, "Edit", self.edit_user, User.__name__, "edit", 90, 25)

        vbox.addLayout(name_layout)
        vbox.addLayout(surname_layout)
        vbox.addLayout(address_layout)
        vbox.addLayout(phone_layout)
        vbox.addLayout(mail_layout)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Edit user")

        self.show()

    def edit_user(self):
        dic = dict()
        dic["name"] = self.name_edit.text()
        dic["surname"] = self.surname_edit.text()
        dic["address"] = self.address_edit.text()
        dic["phone"] = int(self.phone_edit.text())
        dic["email"] = self.mail_edit.text()
        dic["group"] = self.user.group

        User.edit(self.user.card_id, dic)
        self.app.el.fire(EventManager.Events.user_changed, {"id": self.user.card_id})
        self.close()
