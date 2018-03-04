from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, \
    QGroupBox, QTableWidgetItem, QAbstractItemView
from managers.user_manager import User
from gui.UserEdit import UserEdit
from managers.booking_system import Booking_system


class UserInfo(QWidget):
    def __init__(self, userObj):
        super().__init__()
        self.userObj = userObj
        self.user_edit = UserEdit(self.userObj)
        self._set_up_ui()

    def set_up_table(self, table):
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setColumnCount(7)

        ID_item = QTableWidgetItem("ID")
        table.setHorizontalHeaderItem(0, ID_item)

        ser_card_item = QTableWidgetItem("Card ID")
        table.setHorizontalHeaderItem(1, ser_card_item)

        copy_item = QTableWidgetItem("Copy ID")
        table.setHorizontalHeaderItem(2, copy_item)

        check_out_item = QTableWidgetItem("Checked out date")
        table.setHorizontalHeaderItem(3, check_out_item)

        give_lib_item = QTableWidgetItem("Checked out by")
        table.setHorizontalHeaderItem(4, give_lib_item)

        return_item = QTableWidgetItem("Return date")
        table.setHorizontalHeaderItem(5, return_item)

        return_lib_item = QTableWidgetItem("Returned by")
        table.setHorizontalHeaderItem(6, return_lib_item)

        table.setColumnWidth(0, 30)
        table.setColumnWidth(1, 60)
        table.setColumnWidth(2, 60)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 120)
        table.setColumnWidth(5, 120)
        table.setColumnWidth(6, 120)

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

        history = Booking_system().get_user_history(self.userObj)
        self.history_table = QTableWidget()
        self.history_table.setRowCount(len(history))
        self.set_up_table(self.history_table)
        for i in range(0, len(history)):
            self.history_table.setItem(i, 0, QTableWidgetItem(str(history[i].OperationID)))
            self.history_table.setItem(i, 1, QTableWidgetItem(str(history[i].user.card_id)))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(history[i].copy.CopyID)))
            self.history_table.setItem(i, 3, QTableWidgetItem(str(history[i].date_check_out)))
            self.history_table.setItem(i, 4, QTableWidgetItem(str(history[i].librarian_co)))
            self.history_table.setItem(i, 5, QTableWidgetItem(str(history[i].date_return)))
            self.history_table.setItem(i, 6, QTableWidgetItem(str(history[i].librarian_re)))

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