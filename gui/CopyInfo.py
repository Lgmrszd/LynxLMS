from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QTableWidget, QAbstractItemView, QTableWidgetItem
from managers.booking_system import *


class CopyInfo(QWidget):
    def __init__(self, copy, on_edit):
        super().__init__()
        self.copy = copy
        self._on_edit = on_edit
        self.bs = Booking_system()
        self.his = self.bs.get_copy_history(copy)
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        vbox = QVBoxLayout()

        self.book_id = QLabel("ID: " + str(self.copy.CopyID))
        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        edit_button = QPushButton("Copy edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit)

        self.fields = dict()
        dic = {'storage': str, 'checked_out': bool}
        for i in dic:
            line_item = QLabel(str(getattr(self.copy, i)))
            self.fields[i] = line_item
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(100)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)
            if dic[i] == bool:
                line_item.setText(str(int(getattr(self.copy, i))))

        self.table = QTableWidget()
        self._set_up_table(self.table)
        vbox.addWidget(self.table)

        vbox.addStretch()

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(edit_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Copy info")

    def _set_up_table(self, table):
        #table.doubleClicked.connect(self._cell_clicked_event)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setColumnCount(4)
        table.setRowCount(len(self.his))

        ID_item = QTableWidgetItem("ID")
        table.setHorizontalHeaderItem(0, ID_item)

        ser_card_item = QTableWidgetItem("Card ID")
        table.setHorizontalHeaderItem(1, ser_card_item)

        check_out_item = QTableWidgetItem("Checked out date")
        table.setHorizontalHeaderItem(2, check_out_item)

        return_item = QTableWidgetItem("Return date")
        table.setHorizontalHeaderItem(3, return_item)

        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 50)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(2, 120)

        for i in range(0, len(self.his)):
            self._row_update(i)

    def _row_update(self, row):
        self.table.setItem(row, 0, QTableWidgetItem(str(int(self.his[row].OperationID))))
        print(self.his[row].user)
        self.table.setItem(row, 1, QTableWidgetItem(str(int(self.his[row].user.card_id))))
        self.table.setItem(row, 2, QTableWidgetItem(str(self.his[row].date_check_out)))
        self.table.setItem(row, 3, QTableWidgetItem(str(self.his[row].date_return)))

    def edit(self):
        pass
