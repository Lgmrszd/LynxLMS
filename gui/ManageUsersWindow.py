from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog, QComboBox
from gui.UserInfo import UserInfo

class ManageUsersWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()
        self.user_infos = []

    def _set_up_table(self):
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setColumnCount(2)
        self.result_table.setRowCount(15)

        ID_item = QTableWidgetItem("ID")
        self.result_table.setHorizontalHeaderItem(0, ID_item)

        user_name_item = QTableWidgetItem("Name and surname")
        self.result_table.setHorizontalHeaderItem(1, user_name_item)

        self.result_table.setColumnWidth(0, 80)
        self.result_table.setColumnWidth(1, 630)

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

        prev_button = QPushButton("Prev")
        prev_button.clicked.connect(self.prev_page)
        self.page_num = 1
        self.page_num_label = QLabel("")
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
        self.setWindowTitle('Manage users')

    def cell_clicked_event(self, event):
        userInfo = UserInfo(None)
        userInfo.show()
        self.user_infos.append(userInfo)

    def click_search_button(self):
        pass

    def prev_page(self):
        pass

    def next_page(self):
        pass

    def get_result(self):
        pass