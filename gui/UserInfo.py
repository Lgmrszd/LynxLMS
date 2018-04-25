from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTableWidget, \
    QGroupBox, QTableWidgetItem, QAbstractItemView, QInputDialog

from gui.GUITools import add_button
from gui.UserEdit import UserEdit
from gui.Window import Window
from gui.EventManager import EventManager
from managers.user_manager import User


class UserInfo(Window):
    def __init__(self, app, user):
        self.bs = app.bs
        self.user = user
        super().__init__(app)
        self.app.el.register(self.reopen, EventManager.Events.user_changed, self)

    def reopen(self, id):
        if id != self.user.card_id:
            return
        self.close()
        self.app.open_window(UserInfo, {"user": User.get_by_id(self.user.card_id)})

    def compare_window(self, param: dict):
        return self.user.card_id == param["user"].card_id

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
        window_size_x = 700
        window_size_y = 650

        self.user_id = QLabel("ID: " + str(self.user.card_id))
        self.address_label = QLabel("Address: " + str(self.user.address))
        self.phone_label = QLabel("Phone: " + str(self.user.phone))
        self.mail_label = QLabel("Email: " + str(self.user.email))

        fine_button = QPushButton("Pay fine")
        fine_button.setFixedWidth(90)
        fine_button.setFixedHeight(25)
        fine_button.clicked.connect(self.pay_fine)

        history = self.app.bs.get_user_history(self.user)
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

        mail_layout = QHBoxLayout()
        mail_layout.addWidget(self.mail_label)
        mail_layout.addStretch()

        last_layout = QHBoxLayout()
        last_layout.addStretch()
        self.delete_button = add_button(last_layout, "Delete", self.delete_user, User.__name__, "remove", 90, 25)
        add_button(last_layout, "Edit", self.edit_user, User.__name__, "edit", 90, 25)
        last_layout.addWidget(fine_button)

        history_table_group = QGroupBox()
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.history_table)
        history_table_group.setLayout(table_layout)

        vbox.addLayout(id_layout)
        vbox.addLayout(address_layout)
        vbox.addLayout(phone_layout)
        vbox.addLayout(mail_layout)
        vbox.addWidget(history_table_group)
        vbox.addLayout(last_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.user.name + " " + self.user.surname + " information")

        self.show()

    def cell_clicked_event(self):
        pass

    def delete_user(self):
        User.remove(self.user.card_id)
        self.close()
        self.app.el.fire(EventManager.Events.user_deleted, {"id": self.user.card_id})

    def edit_user(self):
        self.app.open_window(UserEdit, {"user": self.user})

    def pay_fine(self):
        mo, okPressed = QInputDialog.getInt(self, "Amount", "How much")
        if not okPressed:
            return
        self.bs.pay_fine(self.user, mo)
        self.app.el.fire(EventManager.Events.fine_paid, {"id": self.user.card_id})
