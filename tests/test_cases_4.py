import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout
from PyQt5 import QtCore
from time import sleep
from gui.Authorisation import Authorization
from gui.MainWindow import MainWindow
import db_config
from managers import auth


admin_data = {
    "login": "a1",
    "password": "a1_pass",
    "privilege": 99,
    "info": "custom admin (cannot create)"
}


l1_data = {
    "login": "l1",
    "password": "l1_pass",
    "privilege": 1,
    "info": "l1 librarian"
}

l2_data = {
    "login": "l2",
    "password": "l2_pass",
    "privilege": 2,
    "info": "l2 librarian"
}

l3_data = {
    "login": "l3",
    "password": "l3_pass",
    "privilege": 3,
    "info": "l3 librarian"
}


def setup_db():
    db_fname = "test_database.db"
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
    qtbot.waitForWindowShown(auth_window.pass_edit)
    sleep(0.2)
    qtbot.mouseClick(auth_window.login_button, QtCore.Qt.LeftButton)
    assert MainWindow in auth_window.app.windows
    qtbot.addWidget(auth_window.app.windows[MainWindow][0])
    return auth_window


def setup_login(qtbot):
    return setup_login_custom(qtbot, "admin", "pass")


def test_case_1():
    setup_db()
    res = auth.AuthUsers.add(("admin", "pass"), **admin_data)
    assert res == 2


def test_case_2():
    setup_db()
    res = auth.AuthUsers.add(("admin", "pass"), **l1_data)
    assert res == 0
    res = auth.AuthUsers.add(("admin", "pass"), **l2_data)
    assert res == 0
    res = auth.AuthUsers.add(("admin", "pass"), **l3_data)
    assert res == 0


def test_case_3(qtbot):
    test_case_2()
    auth_window = setup_login_custom(qtbot, l1_data["login"], l1_data["password"])

    main_window = auth_window.app.windows[MainWindow][0]
    # main_window.switch_search_window()

    qtbot.stopForInteraction()

