from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox
from managers.doc_manager import *

class BookInfo(QWidget):
    def __init__(self, doc):
        super().__init__()
        self._set_up_ui(doc)


    def _set_up_ui(self, doc):
        window_size_x = 400
        window_size_y = 400

        self.book_id = QLabel("ID: "+str(doc.DocumentID))
        vbox = QVBoxLayout()

        self.book_name = QLabel("<h1>"+doc.title+"</h1>")
        self.book_name.setFixedWidth(window_size_x - 20)
        self.book_name.setWordWrap(True)


        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        dic = type(doc).get_fields_dict()
        dic.pop("DocumentID")

        for i in dic:
            line_item = QLabel(str(getattr(doc, i)))
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(60)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)

        vbox.addStretch()


        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Book information')