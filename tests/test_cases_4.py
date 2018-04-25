import shutil
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog, QDialogButtonBox, QTableWidget, QPushButton
from time import sleep
from gui.Authorisation import Authorization
from gui.MainWindow import MainWindow
from gui.AddDocument import AddDocument
from gui.TaskWindow import Dialog
from gui.BookInfo import BookInfo
from gui.AddUser import AddUser
import db_config
import datetime
from managers import auth, user_manager, doc_manager, booking_system, task_manager, event_manager


docs_data = {
    "books": {
        "d1": {
            "title": "Introduction to Algorithms",
            "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein",
            "publisher": "MIT Press",
            "year": 2009,
            "edition": "Third edition",
            "cost": 5000,
            "keywords": "Algorithms, Data Structures, Complexity, Computational Theory",
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

patrons_data = {
    "p1": {
        "name": "Sergey",
        "surname": "Afonso",
        "address": "Via Margutta, 3",
        "phone": "30001",
        "group": "Faculty",
        "email": "m.bobrov@innopolis.ru"
    },
    "p2": {
        "name": "Nadia",
        "surname": "Teixeira",
        "address": "Via Sacra, 13",
        "phone": "30002",
        "group": "Faculty",
        "email": "m.bobrov@innopolis.ru"
    },
    "p3": {
        "name": "Elvira",
        "surname": "Espindola",
        "address": "Via del Corso, 22",
        "phone": "30003",
        "group": "Faculty",
        "email": "m.bobrov@innopolis.ru"
    },
    "s": {
        "name": "Andrey",
        "surname": "Velo",
        "address": "Avenida Mazatlan 250",
        "phone": "30004",
        "group": "Students",
        "email": "m.bobrov@innopolis.ru"
    },
    "v": {
        "name": "Veronika",
        "surname": "Rama",
        "address": "Stret Atocha, 27",
        "phone": "30005",
        "group": "Visiting professors",
        "email": "m.bobrov@innopolis.ru"
    }
}

test4_db = "tests/test_database_4_clear.db"
test_new_db = "tests/test_database_4_clear_copy.db"


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


def setup_db(db_fname="tests/test_database.db"):
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
    # qtbot.stopForInteraction()
    assert MainWindow in auth_window.app.windows
    qtbot.addWidget(auth_window.app.windows[MainWindow][0])
    return auth_window


def setup_login(qtbot):
    return setup_login_custom(qtbot, "admin", "pass")


def get_button_by_name(name, parentType = None):
    # Try 3 times
    for i in range(3):
        for widget in QApplication.allWidgets():
            if isinstance(widget, QPushButton):
                if widget.text() == name:
                    if parentType:
                        if isinstance(widget.parent(), parentType):
                            return widget
                    else:
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

    # qtbot.stopForInteraction()


def test_case_4(qtbot):
    lt = lookThread(qtbot)
    lt.start()
    test_case_2()
    l2_data = get_ln_data(2)
    auth_window = setup_login_custom(qtbot, l2_data["login"], l2_data["password"])
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
        sleep(0.5)
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
        for i in range(3):
            lt.add_write_location()
            qtbot.mouseClick(add_doc_b, QtCore.Qt.LeftButton)
            sleep(0.5)
        book_info.close()
    main_window.search_window.close()

    add_user_b = get_button_by_name("Add user")
    assert add_user_b is not None
    patrons = ["s", "p1", "p2", "p3", "v"]
    patrons = {k: v for k, v in patrons_data.items() if k in patrons}
    for k, patron_data in {k: v for k, v in patrons_data.items() if k in patrons}.items():
        qtbot.mouseClick(add_user_b, QtCore.Qt.LeftButton)
        assert AddUser in auth_window.app.windows
        assert len(auth_window.app.windows[AddUser]) > 0
        add_user_window = auth_window.app.windows[AddUser][0]
        assert isinstance(add_user_window, AddUser)
        qtbot.keyClicks(add_user_window.name_edit, patron_data["name"])
        qtbot.keyClicks(add_user_window.surname_edit, patron_data["surname"])
        qtbot.keyClicks(add_user_window.address_edit, patron_data["address"])
        qtbot.keyClicks(add_user_window.phone_edit, patron_data["phone"])
        qtbot.keyClicks(add_user_window.mail_edit, patron_data["email"])
        add_user_window.group_combo_box.setCurrentIndex(add_user_window.group_combo_box.findText(patron_data["group"]))
        add_user_confirm_b = get_button_by_name("Add", AddUser)
        qtbot.mouseClick(add_user_confirm_b, QtCore.Qt.LeftButton)

    users = user_manager.User.get_list(5, 1)
    assert len(users) == 5
    users_by_name = {v["name"]: v for k, v in patrons.items()}
    db_users_by_name = {i.name: i for i in users}
    for name, user in users_by_name.items():
        assert name in db_users_by_name
        db_user = db_users_by_name[name]
        assert db_user.surname == user["surname"]
        assert db_user.email == user["email"]
    lt.exit()

    books, _ = doc_manager.Book.get_list(5, 1)
    assert len(books) == 3
    books_by_title = {v["title"]: v for k, v in docs_data["books"].items()}
    db_books_by_title = {i.title: i for i in books}
    for title, book in books_by_title.items():
        assert title in db_books_by_title
        db_book = db_books_by_title[title]
        assert db_book.author == book["author"]
        assert len(db_book.get_document_copies()) == 3
    lt.exit()
    shutil.copy("tests/test_database.db", test4_db)


def test_case_5():
    shutil.copy(test4_db, test_new_db)
    db_config.init_db(test_new_db)

    # login as l3
    l3_data = get_ln_data(3)
    auth.Auth.login(l3_data["login"], l3_data["password"])

    books, _ = doc_manager.Book.get_list(5, 1)
    d1 = None
    for book in books:
        if book.title == docs_data["books"]["d1"]["title"]:
            d1 = book

    assert d1 is not None
    assert isinstance(d1, doc_manager.Book)

    d1_copies = d1.get_document_copies()
    d1_copies = [i for i in d1_copies if i.active]
    assert len(d1_copies) == 3

    d1_copy = d1_copies[0]
    assert isinstance(d1_copy, doc_manager.Copy)
    doc_manager.Copy.remove(d1_copy.CopyID)

    # login as l2
    l2_data = get_ln_data(2)
    auth.Auth.login(l2_data["login"], l2_data["password"])

    d1_copies = d1.get_document_copies()
    d1_copies = [i for i in d1_copies if i.active]
    assert len(d1_copies) == 2


def test_case_6():
    shutil.copy(test4_db, test_new_db)
    db_config.init_db(test_new_db)
    l1_data = get_ln_data(1)
    auth.Auth.login(l1_data["login"], l1_data["password"])

    p1 = user_manager.User.get(user_manager.User.name == patrons_data["p1"]["name"])
    p2 = user_manager.User.get(user_manager.User.name == patrons_data["p2"]["name"])
    p3 = user_manager.User.get(user_manager.User.name == patrons_data["p3"]["name"])
    s = user_manager.User.get(user_manager.User.name == patrons_data["s"]["name"])
    v = user_manager.User.get(user_manager.User.name == patrons_data["v"]["name"])
    d3 = doc_manager.Book.get(doc_manager.Book.title == docs_data["books"]["d3"]["title"])

    bsystem = booking_system.Booking_system(l1_data["login"])
    bsystem.check_out(d3, p1)
    bsystem.check_out(d3, p2)
    bsystem.check_out(d3, s)
    bsystem.check_out(d3, v)
    bsystem.check_out(d3, p3)
    access_error = False
    try:
        bsystem.outstanding_request(d3, p3)
    except auth.AccessError:
        access_error = True
    assert access_error


def test_case_7():
    global notified
    notified = False

    def check_notification(code, msg):
        global notified
        notified = True

    shutil.copy(test4_db, test_new_db)
    db_config.init_db(test_new_db)
    l3_data = get_ln_data(3)
    auth.Auth.login(l3_data["login"], l3_data["password"])

    p1 = user_manager.User.get(user_manager.User.name == patrons_data["p1"]["name"])
    p2 = user_manager.User.get(user_manager.User.name == patrons_data["p2"]["name"])
    p3 = user_manager.User.get(user_manager.User.name == patrons_data["p3"]["name"])
    s = user_manager.User.get(user_manager.User.name == patrons_data["s"]["name"])
    v = user_manager.User.get(user_manager.User.name == patrons_data["v"]["name"])
    d3 = doc_manager.Book.get(doc_manager.Book.title == docs_data["books"]["d3"]["title"])

    bsystem = booking_system.Booking_system(l3_data["login"])
    bsystem.check_out(d3, p1)
    bsystem.check_out(d3, p2)
    bsystem.check_out(d3, s)
    bsystem.check_out(d3, v)
    bsystem.check_out(d3, p3)

    d3_c = d3.get_document_copies()

    access_error = False
    try:
        res = bsystem.outstanding_request(d3, p3)
    except auth.AccessError:
        access_error = True
    assert not access_error
    sleep(1)
    event_manager.register_listener("task_ended", check_notification)
    task_manager.timer_function()
    assert notified


def test_case_8(qtbot):
    # This is manual test
    test_case_6()
    auth_window = setup_login_custom(qtbot, "admin", "pass")
    admin_panel_button = get_button_by_name("Admin panel")
    qtbot.mouseClick(admin_panel_button, QtCore.Qt.LeftButton)
    qtbot.stopForInteraction()
    assert True


def test_case_9(qtbot):
    # This is manual test
    test_case_7()
    auth_window = setup_login_custom(qtbot, "admin", "pass")
    admin_panel_button = get_button_by_name("Admin panel")
    qtbot.mouseClick(admin_panel_button, QtCore.Qt.LeftButton)
    qtbot.stopForInteraction()
    assert True


def test_case_10():
    pass
