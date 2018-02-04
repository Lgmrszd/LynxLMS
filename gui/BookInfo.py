from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from gui.BookEdit import BookEdit
from gui.CopiesWindow import *


class BookInfo(QWidget):
    def __init__(self, doc, on_update):
        super().__init__()
        self.doc = doc
        self.on_update = on_update
        self.edit = BookEdit(doc, self._update)
        self.copies = CopiesWindow(doc)
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        self.book_id = QLabel("ID: "+str(self.doc.DocumentID))
        vbox = QVBoxLayout()

        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        dic = type(self.doc).get_fields_dict()
        dic.pop("DocumentID")

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

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(90)
        delete_button.setFixedHeight(25)
        delete_button.clicked.connect(self.delete_document)

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        edit_button_layout.addWidget(delete_button)
        edit_button_layout.addWidget(copies_button)
        edit_button_layout.addWidget(edit_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Document information')

    def _update(self):
        for i in self.fields:
            self.fields[i].setText(str(getattr(self.doc, i)))
        self.on_update()

    def edit_document(self):
        self.edit.show()

    def copy_list(self):
        self.copies.show()

    def delete_document(self):
        reply = QMessageBox.question(self, 'Delete?',
                                           'Do you really want to delete this book?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            return
        type(self.doc).remove(self.doc.DocumentID)
        self.on_update()
        self.close()
