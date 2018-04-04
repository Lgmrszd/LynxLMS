from gui.Queue_window import *
from gui.CopyInfo import *

class CopiesWindow(QWidget):
    __inactive_color = QColor(230, 230, 230)

    def __init__(self, doc, copy_edited_listener):
        super().__init__()
        self._copy_edited_listener = copy_edited_listener
        self.doc = doc
        self.bs = Booking_system()
        self.cl = self.bs.get_document_copies(self.doc)
        self.edits = []
        self.queue = QueueWindow(doc)
        self._set_up_ui()

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

        table.setColumnWidth(0, 80)
        table.setColumnWidth(1, 400)
        table.setColumnWidth(2, 100)

        for i in range(0, len(self.cl)):
            self._row_update(i)

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()
        self.vb = vbox

        self.table = QTableWidget()
        self._set_up_table(self.table)

        vbox.addWidget(self.table)

        add_button = QPushButton("Add new")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_copy)

        book_button = QPushButton("Check out")
        book_button.setFixedWidth(90)
        book_button.setFixedHeight(25)
        book_button.clicked.connect(self.check_out)

        queue_button = QPushButton("Queue")
        queue_button.setFixedWidth(90)
        queue_button.setFixedHeight(25)
        queue_button.clicked.connect(self.show_queue)

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        edit_button_layout.addWidget(queue_button)
        edit_button_layout.addWidget(book_button)
        edit_button_layout.addWidget(add_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Copies of "+self.doc.title)

    def _copy_edited(self, r):
        self._row_update(r)
        self._copy_edited_listener(self.cl[r].CopyID)

    def update_copy_window(self, copy_id):
        for i in range(len(self.edits)):
            if self.edits[i].copy.CopyID == copy_id:
                self.edits[i].update()
                self._copy_edited_listener(None)
        for i in range(self.table.rowCount()):
            self._row_update(i)

    def _cell_clicked_event(self, event):
        r = event.row()
        for i in self.edits:
            if i.copy.CopyID == self.cl[r].CopyID:
                i.close()
                self.edits.remove(i)
                break
        copy_edit_window = CopyInfo(self.cl[r], lambda: self._copy_edited(r))
        copy_edit_window.show()
        self.edits.append(
            copy_edit_window)  # to prevent deletion of copy_edit_window, because copy_edit_window is local variable

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
        # !!!
        # !!!
        self.bs.proceed_free_copy(c, gui.MainWindow.MainWindow.librarian)
        # Kostyl ochen' bolshoy
        # !!!
        # !!!
        self.queue.get_result()
        self.cl = self.bs.get_document_copies(self.doc)
        self.table.setRowCount(len(self.cl))
        self._copy_edited(len(self.cl)-1)

    def closeEvent(self, ev):
        for i in self.edits:
            i.close()
        self.queue.close()
        ev.accept()

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
        (err, res) = self.bs.check_out(self.doc, usr, gui.MainWindow.MainWindow.librarian)
        if err > 0:
            msg = QMessageBox()
            msgs = {7: "User is already in the queue",
                    6: "User already has copy of this document",
                    4: "User is deleted", 3: "Document is not active", 2: "Document is referenced",
                    1: "User has been added to the queue"}
            msg.setText(msgs[err])
            msg.exec_()
            return

        self.queue.get_result()

        for i in self.edits:
            if i.copy.CopyID == res.copy.CopyID:
                i.his = i.bs.get_copy_history(i.copy)
                i.table.setRowCount(len(i.his))
                i._row_update(len(i.his) - 1)
                i._on_edit()
                return

        # if we do not have window we should manually update the state
        for i in range(len(self.cl)):
            if self.cl[i].CopyID == res.copy.CopyID:
                self._copy_edited(i)
                return

    def show_queue(self):
        self.queue.setVisible(not self.queue.isVisible())
