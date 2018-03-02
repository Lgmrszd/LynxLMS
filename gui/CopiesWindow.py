from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from managers.booking_system import *
from managers.doc_manager import *
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
        self._set_up_ui()

    def _row_update(self, row):
        self.cl[row] = Copy.get(Copy.CopyID == self.cl[row].CopyID)
        self.table.setItem(row, 0, QTableWidgetItem(str(self.cl[row].CopyID)))
        self.table.setItem(row, 1, QTableWidgetItem(str(self.cl[row].storage)))
        self.table.setItem(row, 2, QTableWidgetItem(str(int(self.cl[row].checked_out))))
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

        author_item = QTableWidgetItem("Checked out")
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

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        edit_button_layout.addWidget(add_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Copies of "+self.doc.title)

    def _copy_edited(self, r):
        self._row_update(r)
        self._copy_edited_listener()

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
        self.cl = self.bs.get_document_copies(self.doc)
        self.table.setRowCount(len(self.cl))
        self._copy_edited(len(self.cl)-1)

    def closeEvent(self, ev):
        for i in self.edits:
            i.close()
        ev.accept()
