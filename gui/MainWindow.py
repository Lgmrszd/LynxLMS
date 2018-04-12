import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from gui.GUITools import add_button


class MainWindow(QWidget):
    librarian = ""

    def __init__(self):
        super().__init__()
        # self.search_window = SearchWindow(self._s_copy_changed, self)
        # self.history_window = HistoryWindow(self._h_copy_changed)
        # self.manage_users = ManageUsersWindow()
        # self.manage_groups = ManageGroupsWindow()
        self._set_up_ui()

    def closeEvent(self, QCloseEvent):
        """вызывается при close event"""
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

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(hbox)
        add_button(vbox, "Search documents", self.switch_search_window)
        add_button(vbox, "Add document", self.open_add_document_window)
        add_button(vbox, "Manage groups", self.open_groups_window)
        add_button(vbox, "Add group", self.open_add_group)
        add_button(vbox, "Manage users", self.open_manage_users_window)
        add_button(vbox, "Add user", self.open_add_user_window)
        add_button(vbox, "Show history", self.open_history_window)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setFixedSize(window_size_x, window_size_y)
        self._center()
        self.setWindowTitle('Librarian application')

    def _center(self):
        """ставит окно в центр"""
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
        self.search_window.get_result()
        self.search_window.update_page()

    def open_add_document_window(self):
        # add_document = AddDocument(lambda: self._add_window_closed(add_document))
        # if add_document.type is None:
        #     return
        # add_document.show()
        # self.add_documents.append(add_document)
        pass

    def open_manage_users_window(self):
        if self.manage_users.isHidden():
            self.manage_users.show()
        else:
            self.manage_users.hide()

    def open_add_user_window(self):
        # add_user = AddUser()
        # add_user.show()
        # self.add_users.append(add_user)
        pass

    def open_history_window(self):
        if self.history_window.isHidden():
            self.history_window.show()
        else:
            self.history_window.hide()

    def open_groups_window(self):
        if self.manage_groups.isHidden():
            self.manage_groups.show()
        else:
            self.manage_groups.hide()

    def open_add_group(self):
        # add_group = AddGroup()
        # add_group.show()
        # self.add_groups.append(add_group)
        pass