from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QTableWidget, QAbstractItemView, QTableWidgetItem, QInputDialog
from managers.doc_manager import *
from managers.booking_system import *
from managers.user_manager import *
import gui.MainWindow


class CopyInfo(QWidget):
    def __init__(self, copy, on_edit):
        super().__init__()
        self.copy = copy
        self._on_edit = on_edit
        self.bs = Booking_system()
        self.his = self.bs.get_copy_history(copy)
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()

        if self.copy.active:
            self.book_id = QLabel("ID: " + str(self.copy.CopyID))
        else:
            self.book_id = QLabel("<font color='red'>ID: " + str(self.copy.CopyID)+"</font>")
        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        self.fields = dict()
        dic = {'storage': str, 'checked_out': bool}
        for i in dic:
            if dic[i] == bool:
                continue
            line_item = QLabel(str(getattr(self.copy, i)))
            self.fields[i] = line_item
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(100)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)

        self.table = QTableWidget()
        self._set_up_table(self.table)
        vbox.addWidget(self.table)

        edit_button = QPushButton("Copy edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit)

        book_button = QPushButton("Check out")
        book_button.setFixedWidth(90)
        book_button.setFixedHeight(25)
        book_button.clicked.connect(self.check_out)

        return_button = QPushButton("Return copy")
        return_button.setFixedWidth(90)
        return_button.setFixedHeight(25)
        return_button.clicked.connect(self.return_book)

        if self.copy.active:
            self.delete_button = QPushButton("Delete")
        else:
            self.delete_button = QPushButton("Restore")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_book)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(self.delete_button)
        add_button_layout.addWidget(edit_button)
        add_button_layout.addWidget(return_button)
        add_button_layout.addWidget(book_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Copy info")

    def _set_up_table(self, table):
        # table.doubleClicked.connect(self._cell_clicked_event)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setColumnCount(6)
        table.setRowCount(len(self.his))

        ID_item = QTableWidgetItem("ID")
        table.setHorizontalHeaderItem(0, ID_item)

        ser_card_item = QTableWidgetItem("Card ID")
        table.setHorizontalHeaderItem(1, ser_card_item)

        check_out_item = QTableWidgetItem("Checked out date")
        table.setHorizontalHeaderItem(2, check_out_item)

        give_lib_item = QTableWidgetItem("Checked out by")
        table.setHorizontalHeaderItem(3, give_lib_item)

        return_item = QTableWidgetItem("Return date")
        table.setHorizontalHeaderItem(4, return_item)

        return_lib_item = QTableWidgetItem("Returned by")
        table.setHorizontalHeaderItem(5, return_lib_item)

        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 50)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 120)
        table.setColumnWidth(5, 120)

        for i in range(0, len(self.his)):
            self._row_update(i)

    def _row_update(self, row):
        self.table.setItem(row, 0, QTableWidgetItem(str(int(self.his[row].OperationID))))
        self.table.setItem(row, 1, QTableWidgetItem(str(int(self.his[row].user.card_id))))
        self.table.setItem(row, 2, QTableWidgetItem(str(self.his[row].date_check_out)))
        self.table.setItem(row, 3, QTableWidgetItem(str(self.his[row].librarian_co)))
        self.table.setItem(row, 4, QTableWidgetItem(str(self.his[row].date_return)))
        self.table.setItem(row, 5, QTableWidgetItem(str(self.his[row].librarian_re)))

    def check_out(self):
        id, okPressed = QInputDialog.getInt(self, "User", "User card ID")
        if not okPressed:
            return
        usr = None
        try:
            usr = User.get_by_id(id)
        except:
            msg = QMessageBox()
            msg.setText("Invalid user card")
            msg.exec_()
            return
        (err, res) = self.bs.check_out(usr, self.copy, gui.MainWindow.MainWindow.librarian)
        msgs = {6: "User already have copy of this document",
                4: "User is deleted", 3: "Copy is not active", 2: "Copy is referenced", 1: "Copy is already checked out"}
        if err > 0:
            msg = QMessageBox()
            msg.setText(msgs[err])
            msg.exec_()
            return
        self.his = self.bs.get_copy_history(self.copy)
        self.table.setRowCount(len(self.his))
        self._row_update(len(self.his)-1)
        self._on_edit()

    def update(self):
        self.copy = Copy.get_by_id(self.copy.CopyID)
        self.his = self.bs.get_copy_history(self.copy)
        self.table.setRowCount(len(self.his))
        self._row_update(len(self.his) - 1)
        if self.copy.active:
            self.book_id.setText("ID: " + str(self.copy.CopyID))
        else:
            self.book_id.setText("<font color='red'>ID: " + str(self.copy.CopyID)+"</font>")
        if self.copy.active:
            self.delete_button.setText("Delete")
        else:
            self.delete_button.setText("Restore")

    def return_book(self):
        if not self.copy.checked_out:
            msg = QMessageBox()
            msg.setText("The copy is not checked out")
            msg.exec_()
            return
        reply = QMessageBox.question(self, 'Return?',
                                     'Do you really want to return this copy?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        self.bs.return_by_copy(self.copy, gui.MainWindow.MainWindow.librarian)
        self.copy = Copy.get(Copy.CopyID == self.copy.CopyID)
        self.his = self.bs.get_copy_history(self.copy)
        self._row_update(len(self.his)-1)
        self._on_edit()

    def delete_book(self):
        if self.copy.active:
            reply = QMessageBox.question(self, 'Delete?',
                                         'Do you really want to delete this copy?', QMessageBox.Yes, QMessageBox.No)
        else:
            reply = QMessageBox.question(self, 'Restore?',
                                         'Do you really want to restore this copy?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.copy.active:
                Copy.remove(self.copy.CopyID)
            else:
                Copy.restore(self.copy.CopyID)
            self._on_edit()
            self.close()

    def edit(self):
        # ToDo edit copy?
        pass
