from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, \
                                                QTableWidget, QAbstractItemView, QTableWidgetItem, QInputDialog
from gui.CopyInfo import CopyInfo
from gui.EventManager import EventManager
from gui.QueueWindow import QueueWindow
from gui.Window import Window
from gui.BookEdit import BookEdit
from managers.doc_manager import Copy
from gui.GUITools import add_button
from managers.user_manager import User


class BookInfo(Window):
    __inactive_color = QColor(230, 230, 230)

    def __init__(self, app, doc):
        self.doc = doc
        self.bs = app.bs
        self.cl = self.bs.get_document_copies(doc)
        super().__init__(app)
        app.el.register(self._update, EventManager.Events.doc_changed, self)
        app.el.register(self.state_changed, EventManager.Events.doc_deletion_state_changed, self)
        app.el.register(self.copy_changed_listener, EventManager.Events.copy_state_changed, self)
        app.el.register(self.copy_state_changed, EventManager.Events.copy_deletion_state_changed, self)
        self.show()

    def compare_window(self, param: dict):
        return param["doc"].DocumentID == self.doc.DocumentID

    def copy_state_changed(self, id):
        copy = Copy.get_by_id(id)
        if copy.docId == self.doc.DocumentID:
            self.copy_changed_listener(id)
            self.state_changed(self.doc.DocumentID)
            self.app.el.fire(EventManager.Events.doc_deletion_state_changed, {"id": self.doc.DocumentID})

    def state_changed(self, id):
        if id != self.doc.DocumentID:
            return
        self.doc = type(self.doc).get_by_id(self.doc.DocumentID)
        if self.doc.active:
            self.delete_button.setVisible(True)
            self.book_id.setText("ID: " + str(self.doc.DocumentID))
        else:
            self.delete_button.setVisible(False)
            self.book_id.setText("<font color='red'>ID: " + str(self.doc.DocumentID) + "</font>")

    def _set_up_ui(self):
        window_size_x = 600
        window_size_y = 600

        if self.doc.active:
            self.book_id = QLabel("ID: "+str(self.doc.DocumentID))
        else:
            self.book_id = QLabel("<font color='red'>ID: " + str(self.doc.DocumentID)+"</font>")
        vbox = QVBoxLayout()

        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        dic = type(self.doc).get_fields_dict()
        dic.pop("DocumentID")
        dic.pop("active")
        dic.pop("requested")

        self.fields = dict()
        for i in dic:
            line_item = QLabel(str(getattr(self.doc, i)))
            self.fields[i] = line_item
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(60)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)

        self.table = QTableWidget()
        self._set_up_table(self.table)

        vbox.addWidget(self.table)

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit_document)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_document)
        if not self.doc.active:
            self.delete_button.setVisible(False)

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        rb = add_button(edit_button_layout, "OR", self.make_or, 90, 25)
        rb.setStyleSheet("background-color: red;")
        edit_button_layout.addWidget(self.delete_button)
        add_button(edit_button_layout, "Queue", self.show_queue, 90, 25)
        add_button(edit_button_layout, "Add copy", self.add_copy, 90, 25)
        add_button(edit_button_layout, "Check out", self.check_out, 90, 25)
        edit_button_layout.addWidget(edit_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        # self.setFixedWidth(window_size_x)
        self.setWindowTitle('Document information: '+self.doc.title)

    def show_queue(self):
        self.app.open_window(QueueWindow, {"doc": self.doc})
        pass

    def make_or(self):
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
        (code, res) = self.bs.outstanding_request(self.doc, usr)
        msg = QMessageBox()
        msgs = {1: "Copy of a document has been checked out",
                2: "There is a free copy",
                0: "Requested"}
        msg.setText(msgs[code])
        msg.exec_()
        if code < 2:
            for i in range(0, len(self.cl)):
                self._row_update(i)
            self.app.el.fire(EventManager.Events.queue_changed, {"id", self.doc.DocmentID})

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
        (err, res) = self.bs.check_out(self.doc, usr)
        if err > 0:
            msg = QMessageBox()
            msgs = {7: "User is already in the queue",
                    6: "User already has copy of this document",
                    4: "User is deleted", 3: "Document is not active", 2: "Document is referenced",
                    1: "User has been added to the queue"}
            msg.setText(msgs[err])
            msg.exec_()
            if err == 1:
                self.app.el.fire(EventManager.Events.queue_changed, {"id": self.doc.DocumentID})
            return
        self.app.el.fire(EventManager.Events.copy_state_changed, {"id": res.copy.CopyID})

    def copy_changed_listener(self, id):
        copy = Copy.get_by_id(id)
        if copy.get_doc().DocumentID == self.doc.DocumentID:
            for i in range(len(self.cl)):
                if self.cl[i].CopyID == id:
                    self._row_update(i)

    def add_copy(self):
        loc, ok = QInputDialog.getText(self, "Enter copy location", "Location:")

        if not ok:
            return
        if len(str(loc)) == 0:
            msg = QMessageBox()
            msg.setText("Empty location")
            msg.exec_()
            return

        c = Copy.add(self.doc)
        c.storage = str(loc)
        c.save()
        self.app.el.fire(EventManager.Events.queue_changed, {"id": self.doc.DocumentID})
        self.app.el.fire(EventManager.Events.copy_added, {"id": c.CopyID})
        self.cl = self.bs.get_document_copies(self.doc)
        self.table.setRowCount(len(self.cl))
        self._row_update(len(self.cl)-1)

    def _update(self, id):
        if id != self.doc.DocumentID:
            return
        for i in self.fields:
            self.fields[i].setText(str(getattr(self.doc, i)))
        self.setWindowTitle('Document information: ' + self.doc.title)

    def _set_up_table(self, table):
        table.doubleClicked.connect(self._cell_clicked_event)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setColumnCount(3)
        table.setRowCount(len(self.cl))

        ID_item = QTableWidgetItem("ID")
        table.setHorizontalHeaderItem(0, ID_item)

        book_name_item = QTableWidgetItem("Storage")
        table.setHorizontalHeaderItem(1, book_name_item)

        author_item = QTableWidgetItem("State")
        table.setHorizontalHeaderItem(2, author_item)

        table.setColumnWidth(0, 60)
        table.setColumnWidth(1, 350)
        table.setColumnWidth(2, 100)

        for i in range(0, len(self.cl)):
            self._row_update(i)

    def _row_update(self, row):
        self.cl[row] = Copy.get(Copy.CopyID == self.cl[row].CopyID)
        self.table.setItem(row, 0, QTableWidgetItem(str(self.cl[row].CopyID)))
        self.table.setItem(row, 1, QTableWidgetItem(str(self.cl[row].storage)))
        state = {0: "free",
                 1: "assigned",
                 2: "checked out"}
        self.table.setItem(row, 2, QTableWidgetItem(state[int(self.cl[row].checked_out)]))
        if not self.cl[row].active:
            self.table.item(row, 0).setBackground(self.__inactive_color)
            self.table.item(row, 1).setBackground(self.__inactive_color)
            self.table.item(row, 2).setBackground(self.__inactive_color)

    def _cell_clicked_event(self, event):
        r = event.row()
        self.app.open_window(CopyInfo, {"copy": self.cl[r]})

    def edit_document(self):
        self.app.open_window(BookEdit, {"doc": self.doc})

    def delete_document(self):
        if not self.doc.active:
            return

        reply = QMessageBox.question(self, 'Delete?',
                                         'Do you really want to delete this document?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            return
        type(self.doc).remove(self.doc.DocumentID)
        for i in self.cl:
            self.app.el.fire(EventManager.Events.copy_deletion_state_changed, {"id": i.CopyID})
