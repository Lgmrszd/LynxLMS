from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox


class BookInfo(QWidget):
    def __init__(self):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 250

        self.book_id = QLabel("ID: 228322")

        self.book_name = QLabel("<h1>The art of QLabel</h1>")
        self.book_name.setFixedWidth(window_size_x - 20)
        self.book_name.setWordWrap(True)

        self.book_author = QLabel("<h2>unknown</h2>")
        self.book_author.setFixedWidth(window_size_x - 20)
        self.book_author.setWordWrap(True)

        self.book_description = QLabel("<h4>In order to show multiple lines in QLabel, right click on QLabel and select 'change rich text'. This brings up dialog where you can type the text as you want to see including enter key. Setting the word wrap is not required for this.If you set the word wrap as well (in QLabel properties) than it will wrap each individual line in the Qlabel if it was longer than the real estate.</h4>")
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