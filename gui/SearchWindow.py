from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog

from gui.BookInfo import BookInfo
from gui.SearchSettings import SearchSettings
from managers.doc_manager import AVMaterial, Book, JournalArticle, Document


class SearchWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()
        self.par = parent

    def closeEvent(self, event):
        self.par.show()

    def set_up_table(self, table):
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setColumnCount(3)
        self.result_table.setRowCount(15)

        ID_item = QTableWidgetItem("ID")
        self.result_table.setHorizontalHeaderItem(0, ID_item)

        book_name_item = QTableWidgetItem("Book name")
        self.result_table.setHorizontalHeaderItem(1, book_name_item)

        author_item = QTableWidgetItem("Author")
        self.result_table.setHorizontalHeaderItem(2, author_item)

        self.result_table.setColumnWidth(0, 80)
        self.result_table.setColumnWidth(1, 380)
        self.result_table.setColumnWidth(2, 250)

    def _set_up_ui(self):
        window_size_x = 800
        window_size_y = 650

        self.list = None
        self.title_col = 1
        self.id_col = 0
        self.author_col = 2

        self.type = "Book"
        self.sort = "New"
        self.indType = 0
        self.indSort = 2

        self.books = []

        self.search_field = QLineEdit("")
        additional_options_button = QPushButton("...")
        additional_options_button.setFixedWidth(20)
        additional_options_button.clicked.connect(self.settings_button_clicked)

        result_group = QGroupBox("")

        self.result_table = QTableWidget()
        self.set_up_table(self.result_table)
        self.result_table.doubleClicked.connect(self.cell_clicked_event)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.get_result)

        prev_button = QPushButton("Prev")
        page_num = QLabel("")
        next_button = QPushButton("Next")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(additional_options_button)
        search_layout.addWidget(search_button)

        in_group_layout = QVBoxLayout()
        in_group_layout.addWidget(self.result_table)
        result_group.setLayout(in_group_layout)

        prev_next_button_layout = QHBoxLayout()
        prev_next_button_layout.addStretch()
        prev_next_button_layout.addWidget(prev_button)
        prev_next_button_layout.addWidget(page_num)
        prev_next_button_layout.addWidget(next_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(search_layout)
        full_layout.addWidget(result_group)
        full_layout.addLayout(prev_next_button_layout)

        self.setLayout(full_layout)

        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Search')

    def cell_clicked_event(self, event):
        print(str(event.row()) + " row clicked")

        if self.list is not None and len(self.list) > event.row():
            book_info_window = BookInfo(self.list[event.row()])
            book_info_window.show()
            self.books.append(book_info_window)  #to prevent deletion of book_info_window, because book_info_window is local variable

    def update_settings(self):
        self.type = self.search_settings.typeBox.currentText()
        self.indType = self.search_settings.typeBox.currentIndex()
        self.sort = self.search_settings.sortBox.currentText()
        self.indSort = self.search_settings.sortBox.currentIndex()

    def settings_button_clicked(self):
        self.search_settings = SearchSettings()
        self.search_settings.typeBox.setCurrentIndex(self.indType)
        self.search_settings.sortBox.setCurrentIndex(self.indSort)
        self.search_settings.exec_()
        self.update_settings()

    def get_result(self):#вызывается при нажатии на кнопку 'search', вызвав 'self.search_field.text()' можно получить тескт из строки поиска
        print('\'' + self.search_field.text() + '\' searched')
        if self.type == "AV":
            self.list = AVMaterial.get_list(15, 1)
        elif self.type == "Book":
            self.list = Book.get_list(15, 1)
        elif self.type == "Journal":
            self.list = JournalArticle.get_list(15, 1)
        elif self.type == "All":
            self.list = Document.get_list(15, 1)
        for i in range(0, len(self.list)):
            self.result_table.setItem(i, self.title_col, QTableWidgetItem(self.list[i].title))
            self.result_table.setItem(i, self.author_col, QTableWidgetItem(self.list[i].author))
        for i in range(len(self.list), 15):
            self.result_table.setItem(i, self.title_col, QTableWidgetItem(""))
            self.result_table.setItem(i, self.author_col, QTableWidgetItem(""))
            self.result_table.setItem(i, self.id_col, QTableWidgetItem(""))