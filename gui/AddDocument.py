from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QInputDialog, QMessageBox
from managers.doc_manager import *
from gui.Window import Window
from gui.EventManager import EventManager
from gui.GUITools import add_button


class AddDocument(Window):
    def __init__(self, app):
        super().__init__(app)
        doc_types = ("Book", "Journal", "AV")
        item, ok = QInputDialog.getItem(self, "Choose type", "", doc_types, 0, False)
        if ok and item:
            self.type = item
        else:
            self.close()
            return
        self._reset_ui()

    def compare_window(self, param: dict) -> bool:
        return False

    def _reset_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()

        self.fields = dict()
        self.types = dict()
        dic = None
        if self.type == "Book":
            dic = Book.get_fields_dict()
        elif self.type == "Journal":
            dic = JournalArticle.get_fields_dict()
        elif self.type == "AV":
            dic = AVMaterial.get_fields_dict()
        dic.pop("DocumentID")
        dic.pop("active")
        dic.pop("requested")

        for i in dic:
            line_item = QLineEdit()
            self.fields[i] = line_item
            self.types[i] = dic[i]
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(60)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)
            if dic[i] == int:
                validator = QIntValidator()
                line_item.setValidator(validator)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button(add_button_layout, "Add", self.add_document, 90, 25)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add " + self.type)

        self.show()

    def add_document(self):
        type = None
        if self.type == "Book":
            type = Book
        elif self.type == "Journal":
            type = JournalArticle
        elif self.type == "AV":
            type = AVMaterial
        dic = dict()
        for i in self.fields:
            dic[i] = self.fields[i].text()
        for i in dic:
            if dic[i] == "" and i != "keywords":
                msg = QMessageBox()
                msg.setText("Empty " + str(i))
                msg.exec_()
                return
            if self.types[i] == int:
                try:
                    int(dic[i])
                except:
                    msg = QMessageBox()
                    msg.setText(str(i)+" should be an integer")
                    msg.exec_()
                    return
        type.add(dic)
        self.app.el.fire(EventManager.Events.doc_added, {})
        self.close()
