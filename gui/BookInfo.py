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

        self.book_name = QLabel("<h1>"+doc.title+"</h1>")
        self.book_name.setFixedWidth(window_size_x - 20)
        self.book_name.setWordWrap(True)

        self.book_author = QLabel("<h2>"+doc.author+"</h2>")
        self.book_author.setFixedWidth(window_size_x - 20)
        self.book_author.setWordWrap(True)

        desc = ""

        fields = type(doc).get_fields()
        for i in Document.__dict__:
            if fields.__contains__(i):
                fields.remove(i)

        for f in fields:
            desc += f + ": " + str(getattr(doc, f)) + "<br><br>"

        self.book_description = QLabel("<h4>"+desc+"</h4>")
        self.book_description.wordWrap()
        self.book_description.setFixedWidth(window_size_x - 20)
        self.book_description.setWordWrap(True)

        book_genres = [QLabel("genre 1"), QLabel("genre 2")]

        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)

        name_box = QGroupBox()
        name_box.setTitle("Book name")
        name_layout = QVBoxLayout()
        name_layout.addWidget(self.book_name)
        name_layout.addStretch(1)
        name_box.setLayout(name_layout)

        author_box = QGroupBox()
        author_box.setTitle("Author")
        author_layout = QVBoxLayout()
        author_layout.addWidget(self.book_author)
        author_layout.addStretch(1)
        author_box.setLayout(author_layout)

        description_box = QGroupBox()
        description_box.setTitle("Book description")
        description_layout = QVBoxLayout()
        description_layout.addWidget(self.book_description)
        description_layout.addStretch(1)
        description_box.setLayout(description_layout)

        vbox = QVBoxLayout()
        vbox.addLayout(top)
        vbox.addWidget(name_box)
        vbox.addWidget(author_box)
        vbox.addWidget(description_box)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Book information')

    def set_book_name(self, book_name):
        self.book_name.setText(book_name)

    def set_book_author(self, book_author):
        self.book_author.setText(book_author)

    def set_book_description(self, book_description):
        self.book_description.setText(book_description)

