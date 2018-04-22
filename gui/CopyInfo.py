from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, \
    QTableWidget, QAbstractItemView, QTableWidgetItem
from managers.doc_manager import *
from managers.booking_system import *
from gui.Window import Window
from gui.EventManager import EventManager
import gui.MainWindow


class CopyInfo(Window):
    def __init__(self, app, copy):
        self.copy = copy
        self.bs = self.app.bs
        self.his = self.bs.get_copy_history(copy)
        super().__init__(app)
        self.app.el.register(self.update, EventManager.Events.copy_state_changed, self)
        self.app.el.register(self.update, EventManager.Events.copy_deletion_state_changed, self)

    def compare_window(self, param: dict):
        return param["copy"].CopyID == self.copy.CopyID

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

        return_button = QPushButton("Return copy")
        return_button.setFixedWidth(90)
        return_button.setFixedHeight(25)
        return_button.clicked.connect(self.return_book)

        renew = QPushButton("Renew")
        renew.setFixedWidth(90)
        renew.setFixedHeight(25)
        renew.clicked.connect(self.renew)

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
        add_button_layout.addWidget(renew)
        add_button_layout.addWidget(return_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.copy.get_doc().title + "'s copy info")

        self.show()

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
        if self.his[row].date_return is None:
            self.table.setItem(row, 4, QTableWidgetItem(str(self.bs.get_max_return_time(self.his[row]))))
        else:
            self.table.setItem(row, 4, QTableWidgetItem(str(self.his[row].date_return)))
        self.table.setItem(row, 5, QTableWidgetItem(str(self.his[row].librarian_re)))

    def update(self, id):
        if id != self.copy.CopyID:
            return
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
        self.app.el.fire(EventManager.Events.copy_state_changed, {"id": self.copy.CopyID})

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
        self.app.el.fire(EventManager.Events.copy_deletion_state_changed, {"id": self.copy.CopyID})

    def renew(self):
        (err, res) = self.bs.renew_by_copy(self.copy, gui.MainWindow.MainWindow.librarian)
        if err > 0:
            msg = QMessageBox()
            msgs = {6: "Copy has already been renewed",
                    5: "Internal error",
                    4: "Copy is not checked out", 3: "Document is requested", 2: "Copy is overdue",
                    1: "Copy is not checked out"}
            msg.setText(msgs[err])
            msg.exec_()
            return
        self.his = self.bs.get_copy_history(self.copy)
        self.table.setRowCount(len(self.his))
        self._row_update(len(self.his) - 2)
        self._row_update(len(self.his) - 1)

    def edit(self):
        # ToDo edit copy?
        pass