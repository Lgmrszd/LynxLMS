from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, \
    QGroupBox, QTableWidgetItem, QAbstractItemView
from managers.user_manager import Group
from gui.GroupEdit import GroupEdit


class GroupInfo(QWidget):
    def __init__(self, group):
        super().__init__()
        self.group = group
        self.group_edit = GroupEdit(group)
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        self.group_id = QLabel("ID: " + str(self.group.id))

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit_group)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(90)
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(self.delete_group)

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
        self.priority_label = QLabel()
        self.priority_label.setText(str(self.group.priority))

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(90)
        edit_button.setFixedHeight(25)
        edit_button.clicked.connect(self.edit_group)

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(90)
        delete_button.setFixedHeight(25)
        delete_button.clicked.connect(self.delete_group)

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

        priority_layout = QHBoxLayout()
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(edit_button)

        vbox.addLayout(name_layout)
        vbox.addLayout(book_ct_layout)
        vbox.addLayout(book_bestseller_ct_layout)
        vbox.addLayout(journal_ct_layout)
        vbox.addLayout(av_ct_layout)
        vbox.addLayout(priority_layout)
        vbox.addLayout(buttons_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.group.name + " information")

    def delete_group(self):
        Group.remove(self.group.id)
        self.close()

    def edit_group(self):
        self.group_edit.show()