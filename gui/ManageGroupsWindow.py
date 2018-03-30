from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog, QComboBox
from gui.UserInfo import UserInfo
from managers.user_manager import User
from managers.group_manager import Group


class ManageGroupsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()
        self.group_infos = []
        self.list = None
        self.click_search_button()

    def _set_up_table(self):
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setColumnCount(7)
        self.result_table.setRowCount(15)

        ID_item = QTableWidgetItem("ID")
        self.result_table.setHorizontalHeaderItem(0, ID_item)

        user_name_item = QTableWidgetItem("Name")
        self.result_table.setHorizontalHeaderItem(1, user_name_item)

        user_surname_item = QTableWidgetItem("book_ct")
        self.result_table.setHorizontalHeaderItem(2, user_surname_item)

        user_address_item = QTableWidgetItem("book_bestseller_ct")
        self.result_table.setHorizontalHeaderItem(3, user_address_item)

        user_phone_item = QTableWidgetItem("journal_ct")
        self.result_table.setHorizontalHeaderItem(4, user_phone_item)

        user_fine_item = QTableWidgetItem("av_ct")
        self.result_table.setHorizontalHeaderItem(5, user_fine_item)

        user_group_item = QTableWidgetItem("priority")
        self.result_table.setHorizontalHeaderItem(6, user_group_item)

        self.result_table.setColumnWidth(0, 100)
        self.result_table.setColumnWidth(1, 115)
        self.result_table.setColumnWidth(2, 115)
        self.result_table.setColumnWidth(3, 95)
        self.result_table.setColumnWidth(4, 95)
        self.result_table.setColumnWidth(5, 95)
        self.result_table.setColumnWidth(6, 95)

    def _set_up_ui(self):
        window_size_x = 800
        window_size_y = 650

        self.search_field = QLineEdit("")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.click_search_button)

        result_group = QGroupBox("")
        self.result_table = QTableWidget()
        self._set_up_table()
        self.result_table.doubleClicked.connect(self.cell_clicked_event)

        self.page_num = 1
        self.page_num_label = QLabel("")
        prev_button = QPushButton("Prev")
        prev_button.clicked.connect(self.prev_page)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_page)

        full_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(search_button)

        in_group_layout = QVBoxLayout()
        in_group_layout.addWidget(self.result_table)
        result_group.setLayout(in_group_layout)

        prev_next_button_layout = QHBoxLayout()
        prev_next_button_layout.addStretch()
        prev_next_button_layout.addWidget(prev_button)
        prev_next_button_layout.addWidget(self.page_num_label)
        prev_next_button_layout.addWidget(next_button)

        full_layout.addLayout(search_layout)
        full_layout.addWidget(result_group)
        full_layout.addLayout(prev_next_button_layout)

        self.setLayout(full_layout)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Manage groups')

    def update_page(self):
        self.page_num_label.setText(str(self.page_num))

    def cell_clicked_event(self, event):
        if self.list is not None and len(self.list) > event.row():
            group_info = GroupInfo(self.list[event.row()]) # class to be added
            group_info.show()
            self.group_infos.append(group_info)

    def click_search_button(self):
        self.page_num = 1
        self.get_result()
        self.update_page()

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

    def get_result(self):
        self.list = Group.get_list(15, self.page_num)

        for i in range(0, len(self.list)):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(self.list[i].id)))
            self.result_table.setItem(i, 1, QTableWidgetItem(self.list[i].name))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(self.list[i].book_ct)))
            self.result_table.setItem(i, 3, QTableWidgetItem(str(self.list[i].book_bestseller_ct)))
            self.result_table.setItem(i, 4, QTableWidgetItem(str(self.list[i].journal_ct)))
            self.result_table.setItem(i, 5, QTableWidgetItem(str(self.list[i].av_ct)))
            self.result_table.setItem(i, 6, QTableWidgetItem(str(self.list[i].priority)))
        for i in range(len(self.list), 15):
            self.result_table.setItem(i, 0, QTableWidgetItem(""))
            self.result_table.setItem(i, 1, QTableWidgetItem(""))
            self.result_table.setItem(i, 2, QTableWidgetItem(""))
            self.result_table.setItem(i, 3, QTableWidgetItem(""))
            self.result_table.setItem(i, 4, QTableWidgetItem(""))
            self.result_table.setItem(i, 5, QTableWidgetItem(""))
            self.result_table.setItem(i, 6, QTableWidgetItem(""))