from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from gui.Window import Window
from gui.EventManager import EventManager


class BookEdit(Window):
    def __init__(self, app, doc):
        self.doc = doc
        super().__init__(app)

    def compare_window(self, param: dict):
        return self.doc.DocumentID == param["doc"].DocumentID

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()

        save_button = QPushButton("Save")
        save_button.setFixedWidth(90)
        save_button.setFixedHeight(25)
        save_button.clicked.connect(self.save_changes)

        self.fields = dict()
        self.types = dict()
        dic = type(self.doc).get_fields_dict()
        dic.pop("DocumentID")
        dic.pop("active")
        dic.pop("requested")

        for i in dic:
            line_item = QLineEdit()
            line_item.setText(str(getattr(self.doc, i)))
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
        add_button_layout.addWidget(save_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Edit: "+self.doc.title)

        self.show()

    def save_changes(self):
        dic = dict()
        for i in self.fields:
            dic[i] = self.fields[i].text()
        for i in dic:
            if dic[i] == "" and i != "keywords":
                msg = QMessageBox()
                msg.setText("Empty " + str(i))
                msg.exec_()
                return
        for i in dic:
            setattr(self.doc, i, dic[i])
        self.doc.save()
        self.app.el.fire(EventManager.Events.doc_changed, {"id": self.doc.DocumentID})
        self.close()
