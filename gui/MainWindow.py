import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from gui.SearchWindow import SearchWindow
from gui.AddDocument import AddDocument
from gui.ManageUsersWindow import ManageUsersWindow

class MainWindow(QWidget):
    librarian = ""

    def __init__(self):
        super().__init__()
        self.search_window = SearchWindow(self)
        self.manage_users = ManageUsersWindow()
        self.add_documents = []
        self._set_up_ui()

    def closeEvent(self, QCloseEvent):#вызывается при close event
        sys.exit(0)

    def librarian_update(self):
        MainWindow.librarian = str(self.librarian_field.text())

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400


        hbox = QHBoxLayout()
        self.librarian_field = QLineEdit("")
        self.librarian_field.textEdited.connect(self.librarian_update)
        lab = QLabel("Librarian: ")
        hbox.addWidget(lab)
        hbox.addWidget(self.librarian_field)

        search_button = QPushButton("Search documents")
        search_button.setFixedHeight(30)
        search_button.clicked.connect(self.switch_search_window)

        manage_users_button = QPushButton("Manage users")
        manage_users_button.setFixedHeight(30)
        manage_users_button.clicked.connect(self.open_manage_users_window)

        add_document_button = QPushButton("Add document")
        add_document_button.setFixedHeight(30)
        add_document_button.clicked.connect(self.open_add_document_window)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(hbox)
        vbox.addWidget(search_button)
        vbox.addWidget(add_document_button)
        vbox.addWidget(manage_users_button)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setFixedSize(window_size_x, window_size_y)
        self._center()
        self.setWindowTitle('Librarian application')

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

    def _add_window_closed(self, window):
        self.add_documents.remove(window)
        self.search_window.click_search_button()

    def open_add_document_window(self):
        add_document = AddDocument(lambda: self._add_window_closed(add_document))
        if add_document.type is None:
            return
        add_document.show()
        self.add_documents.append(add_document)

    def open_manage_users_window(self):
        if self.manage_users.isHidden():
            self.manage_users.show()
        else:
            self.manage_users.hide()