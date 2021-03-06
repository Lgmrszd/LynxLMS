from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel

from gui.GUITools import add_button
from managers.user_manager import Group
from gui.GroupEdit import GroupEdit
from gui.Window import Window
from gui.EventManager import EventManager


class GroupInfo(Window):
    def __init__(self, app, group):
        self.group = group
        super().__init__(app)
        self.app.el.register(self.reopen, EventManager.Events.group_changed, self)

    def reopen(self, id):
        if id != self.group.id:
            return
        self.close()
        self.app.open_window(GroupInfo, {"group": Group.get_by_id(self.group.id)})

    def compare_window(self, param: dict):
        return self.group.id == param["group"].id

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        self.group_id = QLabel("ID: " + str(self.group.id))

        name_label = QLabel("name : ")
        name_label.setFixedWidth(100)
        book_ct_label = QLabel("book_ct : ")
        book_ct_label.setFixedWidth(100)
        book_bestseller_ct_label = QLabel("book_bestseller_ct : ")
        book_bestseller_ct_label.setFixedWidth(100)
        journal_ct_label = QLabel("journal_ct : ")
        journal_ct_label.setFixedWidth(100)
        av_ct_label = QLabel("av_ct : ")
        av_ct_label.setFixedWidth(100)
        book_rt_label = QLabel("book_rt : ")
        book_rt_label.setFixedWidth(100)
        book_bestseller_rt_label = QLabel("book_bestseller_rt : ")
        book_bestseller_rt_label.setFixedWidth(100)
        journal_rt_label = QLabel("journal_rt : ")
        journal_rt_label.setFixedWidth(100)
        av_rt_label = QLabel("av_rt : ")
        av_rt_label.setFixedWidth(100)
        priority_label = QLabel("priority : ")
        priority_label.setFixedWidth(100)

        self.name_label = QLabel()
        self.name_label.setText(self.group.name)
        self.book_ct_label = QLabel()
        self.book_ct_label.setText(str(self.group.book_ct))
        self.book_bestseller_ct_label = QLabel()
        self.book_bestseller_ct_label.setText(str(self.group.book_bestseller_ct))
        self.journal_ct_label = QLabel()
        self.journal_ct_label.setText(str(self.group.journal_ct))
        self.av_ct_label = QLabel()
        self.av_ct_label.setText(str(self.group.av_ct))
        self.book_rt_label = QLabel()
        self.book_rt_label.setText(str(self.group.book_rt))
        self.book_bestseller_rt_label = QLabel()
        self.book_bestseller_rt_label.setText(str(self.group.book_bestseller_rt))
        self.journal_rt_label = QLabel()
        self.journal_rt_label.setText(str(self.group.journal_rt))
        self.av_rt_label = QLabel()
        self.av_rt_label.setText(str(self.group.av_rt))
        self.priority_label = QLabel()
        self.priority_label.setText(str(self.group.priority))

        vbox = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_label)

        book_ct_layout = QHBoxLayout()
        book_ct_layout.addWidget(book_ct_label)
        book_ct_layout.addWidget(self.book_ct_label)

        book_bestseller_ct_layout = QHBoxLayout()
        book_bestseller_ct_layout.addWidget(book_bestseller_ct_label)
        book_bestseller_ct_layout.addWidget(self.book_bestseller_ct_label)

        journal_ct_layout = QHBoxLayout()
        journal_ct_layout.addWidget(journal_ct_label)
        journal_ct_layout.addWidget(self.journal_ct_label)

        av_ct_layout = QHBoxLayout()
        av_ct_layout.addWidget(av_ct_label)
        av_ct_layout.addWidget(self.av_ct_label)

        book_rt_layout = QHBoxLayout()
        book_rt_layout.addWidget(book_rt_label)
        book_rt_layout.addWidget(self.book_rt_label)

        book_bestseller_rt_layout = QHBoxLayout()
        book_bestseller_rt_layout.addWidget(book_bestseller_rt_label)
        book_bestseller_rt_layout.addWidget(self.book_bestseller_rt_label)

        journal_rt_layout = QHBoxLayout()
        journal_rt_layout.addWidget(journal_rt_label)
        journal_rt_layout.addWidget(self.journal_rt_label)

        av_rt_layout = QHBoxLayout()
        av_rt_layout.addWidget(av_rt_label)
        av_rt_layout.addWidget(self.av_rt_label)

        priority_layout = QHBoxLayout()
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        add_button(buttons_layout, "Delete", self.delete_group, Group.__name__, "remove", 90, 25)
        add_button(buttons_layout, "Edit", self.edit_group, Group.__name__, "edit", 90, 25)

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
        vbox.addLayout(buttons_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.group.name + " information")

        self.show()

    def delete_group(self):
        Group.remove(self.group.id)
        self.close()
        self.app.el.fire(EventManager.Events.group_deleted, {"id": self.group.id})

    def edit_group(self):
        self.app.open_window(GroupEdit, {"group": self.group})
