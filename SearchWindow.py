from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton


class SearchWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()
        self.par = parent

    def closeEvent(self, event):
        self.par.show()

    def _set_up_ui(self):
        window_size_x = 800
        window_size_y = 600

        self.search_field = QLineEdit("")
        additional_options_button = QPushButton("...")

        result_group = QGroupBox("")
        self.test_label = QLabel("kek322")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.get_result)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(additional_options_button)

        in_group_layout = QVBoxLayout()
        in_group_layout.addWidget(self.test_label)
        result_group.setLayout(in_group_layout)

        search_button_layout = QHBoxLayout()
        search_button_layout.addStretch()
        search_button_layout.addWidget(search_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(search_layout)
        full_layout.addWidget(result_group)
        full_layout.addLayout(search_button_layout)

        self.setLayout(full_layout)

        self.setFixedSize(window_size_x, window_size_y)
        self.setWindowTitle('Search')

    def get_result(self):#вызывается при нажатии на кнопку 'search', вызвав 'self.search_field.text()' можно получить тескт из строки поиска
        self.test_label.setText(self.test_label.text() + self.search_field.text())