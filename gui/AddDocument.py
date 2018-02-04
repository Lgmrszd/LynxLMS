from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog, QMessageBox
from managers.doc_manager import*


class AddDocument(QWidget):
    def __init__(self):
        super().__init__()
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

        document_title_label = QLabel("title:")
        document_title_label.setFixedWidth(60)
        self.document_title = QLineEdit()

        document_author_label = QLabel("author:")
        document_author_label.setFixedWidth(60)
        self.document_author = QLineEdit()

        document_cost_label = QLabel("cost:")
        document_cost_label.setFixedWidth(60)
        self.document_cost = QLineEdit()
        cost_validator = QIntValidator()
        cost_validator.setBottom(0)
        self.document_cost.setValidator(cost_validator)
        document_keywords_label = QLabel("keywords:")
        document_keywords_label.setFixedWidth(60)
        self.document_keywords = QTextEdit()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_document)

        document_title_layout = QHBoxLayout()
        document_title_layout.addWidget(document_title_label)
        document_title_layout.addWidget(self.document_title)
        vbox.addLayout(document_title_layout)
        document_author_layout = QHBoxLayout()
        document_author_layout.addWidget(document_author_label)
        document_author_layout.addWidget(self.document_author)
        vbox.addLayout(document_author_layout)
        document_cost_layout = QHBoxLayout()
        document_cost_layout.addWidget(document_cost_label)
        document_cost_layout.addWidget(self.document_cost)
        vbox.addLayout(document_cost_layout)
        document_keywords_layout = QHBoxLayout()
        document_keywords_layout.addWidget(document_keywords_label)
        document_keywords_layout.addWidget(self.document_keywords)
        vbox.addLayout(document_keywords_layout)

        self.fields = dict()
        self.types = dict()
        dic = None
        if self.type == "Book":
            dic = Book.get_fields_dict()
        elif self.type == "Journal":
            dic = JournalArticle.get_fields_dict()
        elif self.type == "AV":
            dic = AVMaterial.get_fields_dict()
        for i in Document.__dict__:
            if dic.__contains__(i):
                dic.pop(i)

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
        dic = {"title": self.document_title.text(), "author": self.document_author.text(), "cost": self.document_cost.text(),
                         "keywords": self.document_keywords.toPlainText()}
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