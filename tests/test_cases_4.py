import typing

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog, QDialogButtonBox, QTableWidget, QPushButton, QLineEdit
from time import sleep
from gui.Authorisation import Authorization
from gui.MainWindow import MainWindow
from gui.AddDocument import AddDocument
from gui.TaskWindow import Dialog
from gui.BookInfo import BookInfo
import db_config
import inspect
from managers import auth


docs_data = {
    "books": {
        "d1": {
            "title": "Introduction to Algorithms",
            "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein",
            "publisher": "MIT Press",
            "year": 2009,
            "edition": "Third edition",
            "cost": 5000,
            "keywords": "Algorithms, Data Structures, Complexity, Computational Theory"
        },
        "d2": {
            "title": "Algorithms + Data Structures = Programs",
            "author": "Niklaus Wirth",
            "publisher": "Prentice Hall PTR",
            "year": 1978,
            "edition": "First edition",
            "cost": 5000,
            "keywords": "Algorithms, Data Structures, Search Algorithms, Pascal"
        },
        "d3": {
            "title": "The Art of Computer Programming",
            "author": "Donald E. Knuth",
            "publisher": "Addison Wesley Longman Publishing Co., Inc.",
            "year": 1997,
            "edition": "Third edition",
            "cost": 5000,
            "keywords": "Algorithms, Combinatorial Algorithms, Recursion"
        }
    }
}


class lookThread(QtCore.QThread):
    def __init__(self, qtbot):
        super().__init__()
        self.tasks = []
        self.qtbot = qtbot

    def add_write_location(self):
        self.tasks.append(self.write_location)

    def write_location(self, all_widgets):
        for widget in all_widgets:
            if isinstance(widget, QInputDialog):
                widget.setTextValue("Some Location")
                for widget2 in all_widgets:
                    if isinstance(widget2, QDialogButtonBox):
                        b = widget2.button(QDialogButtonBox.Ok)
                        if b:
                            self.qtbot.mouseClick(b, QtCore.Qt.LeftButton)
                            sleep(0.4)
                            return True
        return False

    def add_choose_book(self):
        self.tasks.append(self.choose_book)

    def choose_book(self, all_widgets):
        for widget in all_widgets:
            if isinstance(widget, QInputDialog):
                widget.setTextValue("Book")
                for widget2 in all_widgets:
                    if isinstance(widget2, QDialogButtonBox):
                        b = widget2.button(QDialogButtonBox.Ok)
                        if b:
                            self.qtbot.mouseClick(b, QtCore.Qt.LeftButton)
                            sleep(0.4)
                            return True
        return False

    def add_choose_av(self):
        self.tasks.append(self.choose_av)

    def choose_av(self, all_widgets):
        for widget in all_widgets:
            if isinstance(widget, QInputDialog):
                widget.setTextValue("AV")
                for widget2 in all_widgets:
                    if isinstance(widget2, QDialogButtonBox):
                        b = widget2.button(QDialogButtonBox.Ok)
                        if b:
                            b.click()
                            return True
        return False

    def add_choose_journal(self):
        self.tasks.append(self.choose_journal)

    def choose_journal(self, all_widgets):
        for widget in all_widgets:
            if isinstance(widget, QInputDialog):
                widget.setTextValue("Journal")
                for widget2 in all_widgets:
                    if isinstance(widget2, QDialogButtonBox):
                        b = widget2.button(QDialogButtonBox.Ok)
                        if b:
                            b.click()
                            return True
        return False

    def tick(self):
        all_widgets = QApplication.allWidgets()
        new_tasks = []
        for task in self.tasks:
            res = task(all_widgets)
            if not res:
                new_tasks.append(task)
        self.tasks = new_tasks
        for widget in all_widgets:
            if isinstance(widget, QMessageBox) and not isinstance(widget, Dialog):
                widget.close()

    def run(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.tick)
        timer.start(500)
        self.exec_()


# add_choose_book = QtCore.pyqtSignal()
# add_choose_book.connect(lookThread.add_choose_book)

def get_ln_data(n):
    res = {
        "login": "l{}",
        "password": "l{}_pass",
        "privilege": 0,
        "info": "Admin"
    }
    names = {1: "Eugenia Rama", 2: "Luie Ramos", 3: "Ramon Valdez"}
    return {k: (names.get(n, v) if k is "info" else v.format(n) if isinstance(v, str) else n) for k, v in res.items()}


def setup_db():
    db_fname = "tests/test_database.db"
    db_config.init_db(db_fname)
    db_config.drop_tables()
    db_config.create_tables()


def setup_login_custom(qtbot, login, password):
    auth_window = Authorization()
    qtbot.addWidget(auth_window)
    auth_window.show()
    qtbot.waitForWindowShown(auth_window)
    qtbot.keyClicks(auth_window.login_edit, login)
    qtbot.keyClicks(auth_window.pass_edit, password)
    qtbot.waitForWindowShown(auth_window)
    sleep(0.2)
    qtbot.mouseClick(auth_window.login_button, QtCore.Qt.LeftButton)
    assert MainWindow in auth_window.app.windows
    qtbot.addWidget(auth_window.app.windows[MainWindow][0])
    return auth_window


def setup_login(qtbot):
    return setup_login_custom(qtbot, "admin", "pass")


def get_button_by_name(name):
        for widget in QApplication.allWidgets():
            if isinstance(widget, QPushButton):
                if widget.text() == name:
                    return widget
        return None


def test_case_1():
    setup_db()
    res = auth.AuthUsers.add(("admin", "pass"), **get_ln_data(99))
    assert res == 2


def test_case_2():
    setup_db()
    for i in range(1, 4):
        res = auth.AuthUsers.add(("admin", "pass"), **get_ln_data(i))
        assert res == 0


def test_case_3(qtbot):
    test_case_2()
    l1_data = get_ln_data(1)
    auth_window = setup_login_custom(qtbot, l1_data["login"], l1_data["password"])

    main_window = auth_window.app.windows[MainWindow][0]
    # main_window.switch_search_window()

    qtbot.stopForInteraction()


def test_case_4(qtbot):
    lt = lookThread(qtbot)
    lt.start()
    test_case_2()
    l1_data = get_ln_data(2)
    auth_window = setup_login_custom(qtbot, l1_data["login"], l1_data["password"])
    main_window = auth_window.app.windows[MainWindow][0]
    sleep(1)
    # Add books
    add_doc_b = get_button_by_name("Add document")
    assert add_doc_b is not None
    for book_info in docs_data["books"].values():
        lt.add_choose_book()
        qtbot.mouseClick(add_doc_b, QtCore.Qt.LeftButton)
        assert AddDocument in auth_window.app.windows
        assert len(auth_window.app.windows[AddDocument]) > 0
        add_doc_window = auth_window.app.windows[AddDocument][0]
        for k, v in book_info.items():
            add_doc_window.fields[k].setText(str(v))
        qtbot.waitForWindowShown(add_doc_window)
        sleep(0.2)
        add_doc_confirm_b = get_button_by_name("Add")
        assert add_doc_confirm_b is not None
        qtbot.mouseClick(add_doc_confirm_b, QtCore.Qt.LeftButton)

    main_window.search_window.show()
    table = main_window.search_window.result_table
    assert isinstance(table, QTableWidget)
    for row_num in range(3):
        x_pos = table.columnViewportPosition(1) + 2
        y_pos = table.rowViewportPosition(row_num) + 2
        vport = table.viewport()
        qtbot.mouseClick(vport, QtCore.Qt.LeftButton, pos=QtCore.QPoint(x_pos, y_pos))
        qtbot.mouseDClick(vport, QtCore.Qt.LeftButton, pos=QtCore.QPoint(x_pos, y_pos))
        assert BookInfo in auth_window.app.windows
        book_info = auth_window.app.windows[BookInfo][0]
        assert isinstance(book_info, BookInfo)
        add_doc_b = get_button_by_name("Add copy")
        assert add_doc_b is not None
        lt.add_write_location()
        qtbot.mouseClick(add_doc_b, QtCore.Qt.LeftButton)
        sleep(0.5)
        book_info.close()
    main_window.search_window.close()


    qtbot.stopForInteraction()

