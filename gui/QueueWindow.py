from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, \
    QTableWidgetItem, QAbstractItemView
from managers.user_manager import Queue
from gui.Window import Window
from gui.EventManager import EventManager


class QueueWindow(Window):
    __inactive_color = QColor(230, 230, 230)
    __active_color = QTableWidgetItem("").background()

    def __init__(self, app, doc):
        self.doc = doc
        super().__init__(app)
        self.app.el.register(self.update_queue, EventManager.Events.queue_changed, self)

    def compare_window(self, param: dict):
        return self.doc.DocumentID == param["doc"].DocumentID

    def update_queue(self, id):
        if id != self.doc.DocumentID:
            return
        self.get_result()

    def _set_up_ui(self):
        window_size_x = 700
        window_size_y = 650

        self.number = 0
        self.active = 1

        active_label = QLabel("Show:")
        self.activeBox = QComboBox()
        self.activeBox.addItems(["Active", "All", "Not active"])
        self.activeBox.currentIndexChanged.connect(self.update_settings)

        result_group = QGroupBox("")

        self.result_table = QTableWidget()
        self.set_up_table(self.result_table)

        prev_button = QPushButton("Prev")
        prev_button.clicked.connect(self.prev_page)
        self.page_num = 1
        self.page_num_label = QLabel("")
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_page)

        settings_layout = QHBoxLayout()
        settings_layout.addWidget(active_label)
        settings_layout.addWidget(self.activeBox)

        settings_layout.addStretch()

        in_group_layout = QVBoxLayout()
        in_group_layout.addWidget(self.result_table)
        result_group.setLayout(in_group_layout)

        prev_next_button_layout = QHBoxLayout()
        prev_next_button_layout.addStretch()
        prev_next_button_layout.addWidget(prev_button)
        prev_next_button_layout.addWidget(self.page_num_label)
        prev_next_button_layout.addWidget(next_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(settings_layout)
        full_layout.addWidget(result_group)
        full_layout.addLayout(prev_next_button_layout)

        self.setLayout(full_layout)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Queue')
        self.reset_results()

        self.show()

    def set_up_table(self, table):
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setColumnCount(4)
        self.result_table.setRowCount(15)

        ser_card_item = QTableWidgetItem("User ID")
        table.setHorizontalHeaderItem(0, ser_card_item)

        copy_item = QTableWidgetItem("Priority")
        table.setHorizontalHeaderItem(1, copy_item)

        check_out_item = QTableWidgetItem("Assigned copy")
        table.setHorizontalHeaderItem(2, check_out_item)

        give_lib_item = QTableWidgetItem("Time out")
        table.setHorizontalHeaderItem(3, give_lib_item)

        for i in range(15):
            for j in range(self.result_table.columnCount()):
                self.result_table.setItem(i, j, QTableWidgetItem(""))

        table.setColumnWidth(0, 70)
        table.setColumnWidth(1, 70)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 120)

    def update_settings(self):
        self.active = 1-self.activeBox.currentIndex()
        self.get_result()

    def reset_results(self):
        self.page_num = 1
        self.get_result()

    def prev_page(self):
        if self.page_num != 1:
            self.page_num = self.page_num - 1
        self.get_result()

    def next_page(self):
        self.page_num = self.page_num + 1
        self.get_result()
        if len(self.list) == 0:
            self.page_num = self.page_num - 1
            self.get_result()

    def get_result(self):
        self.list, self.number = Queue.get_list(self.doc, 15, self.page_num, self.active)

        for i in range(0, len(self.list)):
            self.result_table.item(i, 0).setText(str(self.list[i].user_id))
            self.result_table.item(i, 1).setText(str(self.list[i].priority))
            if self.list[i].assigned_copy is None:
                self.result_table.item(i, 2).setText("")
                self.result_table.item(i, 3).setText("")
            else:
                self.result_table.item(i, 2).setText(str(self.list[i].assigned_copy.CopyID))
                self.result_table.item(i, 3).setText(str(self.list[i].time_out))

            for j in range(self.result_table.columnCount()):
                if self.list[i].active:
                    self.result_table.item(i, j).setBackground(self.__active_color)
                else:
                    self.result_table.item(i, j).setBackground(self.__inactive_color)

        for i in range(len(self.list), 15):
            for j in range(self.result_table.columnCount()):
                self.result_table.item(i, j).setText("")
                self.result_table.item(i, j).setBackground(self.__active_color)
        self.page_num_label.setText(str(self.page_num) + "/" + str(self.number))
