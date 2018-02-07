from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog, QComboBox

class ManageUsersWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 800
        window_size_y = 650

        self.search_field = QLineEdit("")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.click_search_button)

        result_group = QGroupBox("")
        self.result_table = QTableWidget()

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

    def click_search_button(self):
        pass

    def prev_page(self):
        pass

    def next_page(self):
        pass

    def get_result(self):
        pass