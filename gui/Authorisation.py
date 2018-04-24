from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from managers.auth import Auth, AccessError
from gui.App import App
from managers.booking_system import Booking_system


class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        self._set_up_ui()
        self.app = None

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 300

        hbox = QHBoxLayout()
        hbox.addStretch()

        self.login_label = QLabel("Login")
        self.pass_label = QLabel("Password")

        self.login_edit = QLineEdit("")
        self.pass_edit = QLineEdit("")

        self.status = QLabel("")

        self.login_button = QPushButton("login")
        self.login_button.setFixedHeight(30)
        self.login_button.clicked.connect(self.login)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_edit)
        vbox.addWidget(self.pass_label)
        vbox.addWidget(self.pass_edit)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.status)
        vbox.addStretch()

        hbox.addLayout(vbox)

        hbox.addStretch()

        self.setLayout(hbox)
        self.setFixedSize(window_size_x, window_size_y)
        self._center()
        self.setWindowTitle('Authorization')

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        login = self.login_edit.text()
        password = self.pass_edit.text()
        if len(login) == 0:
            self.status.setText("<font color='red'> Empty login field </font>")
            return
        if len(password) == 0:
            self.status.setText("<font color='red'> Empty password field </font>")
            return
        print(login + " " + password)

        if Auth.login(login, password) != 0:
            self.status.setText("<font color='red'> Incorrect login / password </font>")
            return

        self.close()
        self.app = App(Booking_system(login))
