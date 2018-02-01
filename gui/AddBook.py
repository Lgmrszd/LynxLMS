from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea
from managers.doc_manager import Document


class AddBook(QWidget):
    def __init__(self):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        book_name_label = QLabel("Book name:")
        book_name_label.setFixedWidth(100)
        self.book_name = QLineEdit()
        book_author_label = QLabel("Book author:")
        book_author_label.setFixedWidth(100)
        self.book_author = QLineEdit()
        book_type_label = QLabel("Book type:")
        book_type_label.setFixedWidth(100)
        self.book_type = QComboBox()
        book_genre_label = QLabel("Book genre:")
        book_genre_label.setFixedWidth(100)
        self.book_genre = QComboBox()
        book_description_label = QLabel("Book description:")
        book_description_label.setFixedWidth(100)
        self.book_description = QTextEdit()
        book_is_bestseller = QCheckBox()
        book_is_bestseller.setText("Is bestseller")
        book_details_label = QLabel("Details:")
        self.book_details = QTextEdit()
        add_button = QPushButton("Add book")
        add_button.clicked.connect(self.add_book)

        vbox = QVBoxLayout()
        book_name_layout = QHBoxLayout()
        book_name_layout.addWidget(book_name_label)
        book_name_layout.addWidget(self.book_name)
        vbox.addLayout(book_name_layout)
        book_author_layout = QHBoxLayout()
        book_author_layout.addWidget(book_author_label)
        book_author_layout.addWidget(self.book_author)
        vbox.addLayout(book_author_layout)
        book_type_layout = QHBoxLayout()
        book_type_layout.addWidget(book_type_label)
        book_type_layout.addWidget(self.book_type)
        vbox.addLayout(book_type_layout)
        book_genre_layout = QHBoxLayout()
        book_genre_layout.addWidget(book_genre_label)
        book_genre_layout.addWidget(self.book_genre)
        vbox.addLayout(book_genre_layout)
        vbox.addWidget(book_is_bestseller)
        vbox.addWidget(book_description_label)
        vbox.addWidget(self.book_description)
        vbox.addWidget(book_details_label)
        vbox.addWidget(self.book_details)
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(add_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add book")

    def add_book(self):
        Document.add(self.book_name.text(), self.book_author.text(), 123, self.book_details.toPlainText())