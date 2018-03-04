from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QGroupBox
from managers.user_manager import User
from gui.UserEdit import UserEdit


class UserInfo(QWidget):
    def __init__(self, userObj):
        super().__init__()
        self.userObj = userObj
        self.user_edit = UserEdit(self.userObj)
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        self.user_id = QLabel("ID: " + str(self.userObj.card_id))
        self.address_label = QLabel("Address: " + str(self.userObj.address))
        self.phone_label = QLabel("Phone: " + str(self.userObj.phone))

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit_user)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_user)

        self.history_table = QTableWidget()

        self.history_table.doubleClicked.connect(self.cell_clicked_event)

        vbox = QVBoxLayout()

        id_layout = QHBoxLayout()
        id_layout.addStretch()
        id_layout.addWidget(self.user_id)

        address_layout = QHBoxLayout()
        address_layout.addWidget(self.address_label)
        address_layout.addStretch()

        phone_layout = QHBoxLayout()
        phone_layout.addWidget(self.phone_label)
        phone_layout.addStretch()

        last_layout = QHBoxLayout()
        last_layout.addStretch()
        last_layout.addWidget(self.delete_button)
        last_layout.addWidget(edit_button)

        history_table_group = QGroupBox()
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.history_table)
        history_table_group.setLayout(table_layout)

        vbox.addLayout(id_layout)
        vbox.addLayout(address_layout)
        vbox.addLayout(phone_layout)
        vbox.addWidget(history_table_group)
        vbox.addLayout(last_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.userObj.name + " " + self.userObj.surname + " information")

    def cell_clicked_event(self):
        pass

    def delete_user(self):
        User.remove(self.userObj.card_id)
        self.close()

    def edit_user(self):
        self.user_edit.show()
        self.user_id.setText("ID: " + str(self.userObj.card_id))
        self.address_label.setText("Address: " + str(self.userObj.address))
        self.phone_label.setText("Phone: " + str(self.userObj.phone))
        self.setWindowTitle(self.userObj.name + " " + self.userObj.surname + " information")