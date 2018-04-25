from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from managers.group_manager import Group
from gui.Window import Window
from gui.EventManager import EventManager
from gui.GUITools import add_button


class AddGroup(Window):
    def __init__(self, app):
        super().__init__(app)

    def compare_window(self, param: dict):
        return False

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        name_label = QLabel("name")
        name_label.setFixedWidth(120)
        book_ct_label = QLabel("book_ct")
        book_ct_label.setFixedWidth(120)
        book_bestseller_ct_label = QLabel("book_bestseller_ct")
        book_bestseller_ct_label.setFixedWidth(120)
        journal_ct_label = QLabel("journal_ct")
        journal_ct_label.setFixedWidth(120)
        av_ct_label = QLabel("av_ct")
        av_ct_label.setFixedWidth(120)
        book_rt_label = QLabel("book_rt")
        book_rt_label.setFixedWidth(120)
        book_bestseller_rt_label = QLabel("book_bestseller_rt")
        book_bestseller_rt_label.setFixedWidth(120)
        journal_rt_label = QLabel("journal_rt")
        journal_rt_label.setFixedWidth(120)
        av_rt_label = QLabel("av_rt")
        av_rt_label.setFixedWidth(120)
        priority_label = QLabel("priority")
        priority_label.setFixedWidth(120)

        self.name_edit = QLineEdit()
        self.book_ct_edit = QLineEdit()
        self.book_bestseller_ct_edit = QLineEdit()
        self.journal_ct_edit = QLineEdit()
        self.av_ct_edit = QLineEdit()
        self.book_rt_edit = QLineEdit()
        self.book_bestseller_rt_edit = QLineEdit()
        self.journal_rt_edit = QLineEdit()
        self.av_rt_edit = QLineEdit()
        self.priority_edit = QLineEdit()

        vbox = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)

        book_ct_layout = QHBoxLayout()
        book_ct_layout.addWidget(book_ct_label)
        book_ct_layout.addWidget(self.book_ct_edit)

        book_bestseller_ct_layout = QHBoxLayout()
        book_bestseller_ct_layout.addWidget(book_bestseller_ct_label)
        book_bestseller_ct_layout.addWidget(self.book_bestseller_ct_edit)

        journal_ct_layout = QHBoxLayout()
        journal_ct_layout.addWidget(journal_ct_label)
        journal_ct_layout.addWidget(self.journal_ct_edit)

        av_ct_layout = QHBoxLayout()
        av_ct_layout.addWidget(av_ct_label)
        av_ct_layout.addWidget(self.av_ct_edit)

        book_rt_layout = QHBoxLayout()
        book_rt_layout.addWidget(book_rt_label)
        book_rt_layout.addWidget(self.book_rt_edit)

        book_bestseller_rt_layout = QHBoxLayout()
        book_bestseller_rt_layout.addWidget(book_bestseller_rt_label)
        book_bestseller_rt_layout.addWidget(self.book_bestseller_rt_edit)

        journal_rt_layout = QHBoxLayout()
        journal_rt_layout.addWidget(journal_rt_label)
        journal_rt_layout.addWidget(self.journal_rt_edit)

        av_rt_layout = QHBoxLayout()
        av_rt_layout.addWidget(av_rt_label)
        av_rt_layout.addWidget(self.av_rt_edit)

        priority_layout = QHBoxLayout()
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_edit)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button(add_button_layout, "Add", self.add_user, Group.__name__, "add", 90, 25)

        vbox.addLayout(name_layout)
        vbox.addLayout(book_ct_layout)
        vbox.addLayout(book_bestseller_ct_layout)
        vbox.addLayout(journal_ct_layout)
        vbox.addLayout(av_ct_layout)
        vbox.addLayout(book_rt_layout)
        vbox.addLayout(book_bestseller_rt_layout)
        vbox.addLayout(journal_rt_layout)
        vbox.addLayout(av_rt_layout)
        vbox.addLayout(priority_layout)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add group")

        self.show()

    def add_user(self):
        dic = dict()
        dic["name"] = self.name_edit.text()
        dic["book_ct"] = int(self.book_ct_edit.text())
        dic["book_bestseller_ct"] = int(self.book_bestseller_ct_edit.text())
        dic["journal_ct"] = int(self.journal_ct_edit.text())
        dic["av_ct"] = int(self.av_ct_edit.text())
        dic["book_rt"] = int(self.book_rt_edit.text())
        dic["book_bestseller_rt"] = int(self.book_bestseller_rt_edit.text())
        dic["journal_rt"] = int(self.journal_rt_edit.text())
        dic["av_rt"] = int(self.av_rt_edit.text())
        dic["priority"] = int(self.priority_edit.text())

        Group.add(dic)
        self.app.el.fire(EventManager.Events.group_added, {})
        self.close()
