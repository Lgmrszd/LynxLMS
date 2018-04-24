from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QMessageBox

from gui import TaskWindow
from gui.AddUser import AddUser
from gui.EventManager import EventManager
from gui.ManageUsersWindow import ManageUsersWindow
from gui.AddGroup import AddGroup
from gui.GUITools import add_button
from gui.HistoryWindow import HistoryWindow
from gui.ManageGroupsWindow import ManageGroupsWindow
from gui.Window import Window
from gui.AddDocument import AddDocument
from gui.SearchWindow import SearchWindow
from PyQt5.QtWidgets import QApplication
from managers import auth

class MainWindow(Window):
    def __init__(self, app):
        super().__init__(app)
        self.dialog = None
        app.el.register(self.task_show, EventManager.Events.task_started, self)
        app.el.register(self.task_update, EventManager.Events.task_completeness, self)
        app.el.register(self.task_crash, EventManager.Events.task_crashed, self)
        app.el.register(self.task_finish, EventManager.Events.task_finished, self)

    def task_show(self, name):
        self.dialog = TaskWindow.Dialog(name)
        self.dialog.show()

    def task_update(self, progress):
        self.dialog.upd(progress)

    def task_crash(self, message):
        self.dialog.finish("<font color='red'>"+message+"</font>")

    def task_finish(self, message):
        self.dialog.finish(message)

    def closeEvent(self, QCloseEvent):
        """вызывается при close event"""
        super(MainWindow, self).closeEvent(QCloseEvent)
        QApplication.instance().exit()

    def _set_up_ui(self):
        self.search_window = self.app.open_window(SearchWindow, {})
        self.history_window = self.app.open_window(HistoryWindow, {})
        self.manage_users = self.app.open_window(ManageUsersWindow, {})
        self.manage_groups = self.app.open_window(ManageGroupsWindow, {})
        window_size_x = 400
        window_size_y = 400

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        add_button(vbox, "Search documents", self.switch_search_window)
        add_button(vbox, "Add document", self.open_add_document_window)
        add_button(vbox, "Manage groups", self.open_groups_window)
        add_button(vbox, "Add group", self.open_add_group)
        add_button(vbox, "Manage users", self.open_manage_users_window)
        add_button(vbox, "Add user", self.open_add_user_window)
        add_button(vbox, "Show history", self.open_history_window)
        if auth.Auth.get_access_level()[0] == 'admin':
            add_button(vbox, "Admin panel", self.open_admin_panel)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setFixedSize(window_size_x, window_size_y)
        self._center()
        self.setWindowTitle('Librarian application')

        self.show()

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
        self.app.open_window(AddDocument, {})

    def open_manage_users_window(self):
        if self.manage_users.isHidden():
            self.manage_users.show()
        else:
            self.manage_users.hide()

    def open_add_user_window(self):
        self.app.open_window(AddUser, {})

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
        self.app.open_window(AddGroup, {})

    def open_admin_panel(self):
        pass