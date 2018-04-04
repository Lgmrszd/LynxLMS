from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from gui.BookEdit import BookEdit
from gui.CopiesWindow import *


class BookInfo(QWidget):
    def __init__(self, doc, on_update, on_copy_update):
        super().__init__()
        self.doc = doc
        self.on_update = on_update
        self._on_copy_update = on_copy_update
        self.edit = BookEdit(doc, self._update)
        self.copies = CopiesWindow(doc, self._on_copies_update)
        self._set_up_ui()

    def _on_copies_update(self, copy_id):
        self.doc = type(self.doc).get_by_id(self.doc.DocumentID)
        if self.doc.active:
            self.delete_button.setVisible(True)
            self.book_id.setText("ID: " + str(self.doc.DocumentID))
        else:
            self.delete_button.setVisible(False)
            self.book_id.setText("<font color='red'>ID: " + str(self.doc.DocumentID) + "</font>")
        self.on_update()
        self._on_copy_update(copy_id)

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

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

        vbox.addStretch()

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit_document)

        copies_button = QPushButton("Copies")
        copies_button.setFixedWidth(90)
        copies_button.setFixedHeight(25)
        copies_button.clicked.connect(self.copy_list)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_document)
        if not self.doc.active:
            self.delete_button.setVisible(False)

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        edit_button_layout.addWidget(self.delete_button)
        edit_button_layout.addWidget(copies_button)
        edit_button_layout.addWidget(edit_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Document information: '+self.doc.title)

    def _update(self):
        for i in self.fields:
            self.fields[i].setText(str(getattr(self.doc, i)))
        self.setWindowTitle('Document information: ' + self.doc.title)
        self.on_update()

    def edit_document(self):
        self.edit.show()

    def copy_list(self):
        self.copies.show()

    def update_copy_window(self, copy_id):
        self.copies.update_copy_window(copy_id)

    def delete_document(self):
        if not self.doc.active:
            return

        reply = QMessageBox.question(self, 'Delete?',
                                         'Do you really want to delete this document?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            return
        self.edit.close()
        self.copies.close()
        type(self.doc).remove(self.doc.DocumentID)
        self.on_update()
        self.close()


