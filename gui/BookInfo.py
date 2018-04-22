from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from gui.EventManager import EventManager
from gui.Window import Window
from gui.BookEdit import BookEdit


class BookInfo(Window):
    def __init__(self, app, doc):
        self.doc = doc
        super().__init__(app)
        app.el.register(self._update, EventManager.Events.doc_changed, self)
        app.el.register(self.state_changed, EventManager.Events.doc_state_changed, self)
        self.show()

    def compare_window(self, param: dict):
        return param["doc"].DocumentID == self.doc.DocumentID

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

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_document)
        if not self.doc.active:
            self.delete_button.setVisible(False)

        edit_button_layout = QHBoxLayout()
        edit_button_layout.addStretch()
        edit_button_layout.addWidget(self.delete_button)
        edit_button_layout.addWidget(edit_button)
        vbox.addLayout(edit_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Document information: '+self.doc.title)

    def _update(self, id):
        if id != self.doc.DocumentID:
            return
        for i in self.fields:
            self.fields[i].setText(str(getattr(self.doc, i)))
        self.setWindowTitle('Document information: ' + self.doc.title)

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
        self.app.el.fire(EventManager.Events.doc_state_changed, {"id": self.doc.DocumentID})
