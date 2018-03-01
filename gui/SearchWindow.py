from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog, QComboBox, QCheckBox

from gui.BookInfo import BookInfo
from managers.doc_manager import AVMaterial, Book, JournalArticle, Document


class SearchWindow(QWidget):
    __inactive_color = QColor(230,230,230)

    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()
        self.par = parent

    def closeEvent(self, event):
        self.par.show()

    def set_up_table(self):
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
        self.active = 1
        self.indType = 0
        self.indSort = 2

        self.books = []

        self.search_field = QLineEdit("")

        sort_label = QLabel("Sort by:")
        self.sortBox = QComboBox()
        self.sortBox.addItems(["Popular", "Name", "New"])
        self.sortBox.currentIndexChanged.connect(self.update_settings)

        type_label = QLabel("Type:")
        self.typeBox = QComboBox()
        self.typeBox.addItems(["Book", "Journal", "AV"])
        self.typeBox.currentIndexChanged.connect(self.update_settings)

        active_label = QLabel("Show:")
        self.activeBox = QComboBox()
        self.activeBox.addItems(["Active", "All", "Deleted"])
        self.activeBox.currentIndexChanged.connect(self.update_settings)

        result_group = QGroupBox("")

        self.result_table = QTableWidget()
        self.set_up_table()
        self.result_table.doubleClicked.connect(self.cell_clicked_event)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.click_search_button)

        prev_button = QPushButton("Prev")
        prev_button.clicked.connect(self.prev_page)
        self.page_num = 1
        self.page_num_label = QLabel("")
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_page)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(search_button)

        settings_layout = QHBoxLayout()
        settings_layout.addWidget(sort_label)
        settings_layout.addWidget(self.sortBox)
        settings_layout.addWidget(type_label)
        settings_layout.addWidget(self.typeBox)
        settings_layout.addWidget(active_label)
        settings_layout.addWidget(self.activeBox)

        settings_layout.addStretch()

        in_group_layout = QVBoxLayout()
        in_group_layout.addWidget(self.result_table)
        result_group.setLayout(in_group_layout)

        prev_next_button_layout = QHBoxLayout()
        prev_next_button_layout.addStretch()
        prev_next_button_layout.addWidget(prev_button)
        prev_next_button_layout.addWidget(self.page_num_label)
        prev_next_button_layout.addWidget(next_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(search_layout)
        full_layout.addLayout(settings_layout)
        full_layout.addWidget(result_group)
        full_layout.addLayout(prev_next_button_layout)

        self.setLayout(full_layout)

        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Search')
        self.click_search_button()

    def cell_clicked_event(self, event):
        if self.list is not None and len(self.list) > event.row():
            book_info_window = BookInfo(self.list[event.row()], self.get_result)
            book_info_window.show()
            self.books.append(book_info_window)  #to prevent deletion of book_info_window, because book_info_window is local variable

    def update_settings(self):
        self.type = self.typeBox.currentText()
        self.indType = self.typeBox.currentIndex()
        self.sort = self.sortBox.currentText()
        self.indSort = self.sortBox.currentIndex()
        self.active = 1-self.activeBox.currentIndex()
        self.click_search_button()

    def update_page(self):
        self.page_num_label.setText(str(self.page_num)+"/"+str(self.number))

    def prev_page(self):
        if self.page_num != 1:
            self.page_num = self.page_num - 1
        self.get_result()
        self.update_page()

    def next_page(self):
        self.page_num = self.page_num + 1
        self.get_result()
        if len(self.list) == 0:
            self.page_num = self.page_num - 1
            self.get_result()
        self.update_page()

    def click_search_button(self):
        self.page_num = 1
        self.get_result()
        self.update_page()

    def get_result(self):#вызывается при нажатии на кнопку 'search', вызвав 'self.search_field.text()' можно получить тескт из строки поиска
        if self.type == "AV":
            self.list, self.number = AVMaterial.get_list(15, self.page_num, self.active)
        elif self.type == "Book":
            self.list, self.number = Book.get_list(15, self.page_num, self.active)
        elif self.type == "Journal":
            self.list, self.number = JournalArticle.get_list(15, self.page_num, self.active)

        for i in range(0, len(self.list)):
            self.result_table.setItem(i, self.title_col, QTableWidgetItem(self.list[i].title))
            self.result_table.setItem(i, self.author_col, QTableWidgetItem(self.list[i].author))
            self.result_table.setItem(i, self.id_col, QTableWidgetItem(str(self.list[i].DocumentID)))
            if not self.list[i].active:
                self.result_table.item(i, 0).setBackground(self.__inactive_color)
                self.result_table.item(i, 1).setBackground(self.__inactive_color)
                self.result_table.item(i, 2).setBackground(self.__inactive_color)
        for i in range(len(self.list), 15):
            self.result_table.setItem(i, self.title_col, QTableWidgetItem(""))
            self.result_table.setItem(i, self.author_col, QTableWidgetItem(""))
            self.result_table.setItem(i, self.id_col, QTableWidgetItem(""))