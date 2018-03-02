from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog, QMessageBox
from managers.doc_manager import*


class AddDocument(QWidget):
    def __init__(self, on_close_listener):
        super().__init__()
        self._on_close_listener = on_close_listener
        doc_types = ("Book", "Journal", "AV")
        item, ok = QInputDialog.getItem(self, "Choose type", "", doc_types, 0, False)
        if ok and item:
            self.type = item
        else:
            self.type = None
            return
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        vbox = QVBoxLayout()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_document)

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
        add_button_layout.addWidget(add_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add " + self.type)

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
            if dic[i] == "":
                msg = QMessageBox()
                msg.setText("Empty " + str(i))
                msg.exec_()
                return
        type.add(dic)
        self.close()

    def closeEvent(self, ev):
        self._on_close_listener()
        ev.accept()