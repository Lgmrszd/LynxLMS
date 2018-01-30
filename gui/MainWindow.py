import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QVBoxLayout
from gui.SearchWindow import SearchWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.search_window = SearchWindow(self)
        self._set_up_ui()

    def closeEvent(self, QCloseEvent):#вызывается при close event
        sys.exit(0)

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        search_button = QPushButton("Search books")
        search_button.setFixedHeight(30)
        search_button.clicked.connect(self.switch_search_window)
        manage_users_button = QPushButton("Manage users")
        manage_users_button.setFixedHeight(30)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addWidget(search_button)
        vbox.addWidget(manage_users_button)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setFixedSize(window_size_x, window_size_y)
        self._center()
        self.setWindowTitle('Library')

    def _center(self):# ставит окно в центр
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def switch_search_window(self):
        if self.search_window.isHidden():
            self.search_window.show()
        else:
            self.search_window.hide()