from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QComboBox, QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, \
    QTableWidgetItem, QAbstractItemView
from gui.CopyInfo import CopyInfo
from gui.Window import Window
from gui.EventManager import EventManager

class HistoryWindow(Window):
    __inactive_color = QColor(230, 230, 230)
    __overdue_color = QColor(255, 230, 230)
    __active_color = QTableWidgetItem("").background()

    def __init__(self, app):
        super().__init__(app)
        self.app.el.register(self._copy_edited, EventManager.Events.copy_state_changed, self)

    def closeEvent(self, QCloseEvent):
        # To keep it in list of windows in App and EventManager
        # I wish we made this project in Java
        pass

    def _set_up_ui(self):
        window_size_x = 700
        window_size_y = 650

        self.bs = self.app.bs
        self.number = 0

        self.active = 2

        active_label = QLabel("Show:")
        self.activeBox = QComboBox()
        self.activeBox.addItems(["Overdue", "Opened", "All", "Closed"])
        self.activeBox.currentIndexChanged.connect(self.update_settings)

        result_group = QGroupBox("")

        self.result_table = QTableWidget()
        self.set_up_table(self.result_table)
        self.result_table.doubleClicked.connect(self.cell_clicked_event)

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
        self.setWindowTitle('History')
        self.reset_results()

    def set_up_table(self, table):
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setColumnCount(7)
        self.result_table.setRowCount(15)

        ID_item = QTableWidgetItem("ID")
        table.setHorizontalHeaderItem(0, ID_item)

        ser_card_item = QTableWidgetItem("Card ID")
        table.setHorizontalHeaderItem(1, ser_card_item)

        copy_item = QTableWidgetItem("Copy ID")
        table.setHorizontalHeaderItem(2, copy_item)

        check_out_item = QTableWidgetItem("Checked out date")
        table.setHorizontalHeaderItem(3, check_out_item)

        give_lib_item = QTableWidgetItem("Checked out by")
        table.setHorizontalHeaderItem(4, give_lib_item)

        return_item = QTableWidgetItem("Return date")
        table.setHorizontalHeaderItem(5, return_item)

        return_lib_item = QTableWidgetItem("Returned by")
        table.setHorizontalHeaderItem(6, return_lib_item)

        for i in range(15):
            for j in range(self.result_table.columnCount()):
                self.result_table.setItem(i, j, QTableWidgetItem(""))

        table.setColumnWidth(0, 30)
        table.setColumnWidth(1, 60)
        table.setColumnWidth(2, 60)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 120)
        table.setColumnWidth(5, 120)
        table.setColumnWidth(6, 120)

    def update_settings(self):
        self.active = 2-self.activeBox.currentIndex()
        self.get_result()

    def _copy_edited(self, id):
        self.get_result()

    def cell_clicked_event(self, event):
        if self.list is not None and len(self.list) > event.row():
            r = event.row()
            self.app.open_window(CopyInfo, {"copy": self.list[r].copy})

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
        self.list, self.number = self.bs.get_list(15, self.page_num, self.active)

        for i in range(0, len(self.list)):
            self.result_table.item(i, 0).setText(str(self.list[i].OperationID))
            self.result_table.item(i, 1).setText(str(self.list[i].user.card_id))
            self.result_table.item(i, 2).setText(str(self.list[i].copy.CopyID))
            self.result_table.item(i, 3).setText(str(self.list[i].date_check_out))
            self.result_table.item(i, 4).setText(str(self.list[i].librarian_co))
            if self.list[i].date_return is None:
                self.result_table.item(i, 5).setText(str(self.bs.get_max_return_time(self.list[i])))
            else:
                self.result_table.item(i, 5).setText(str(self.list[i].date_return))
            self.result_table.item(i, 6).setText(str(self.list[i].librarian_re))

            for j in range(self.result_table.columnCount()):
                if self.list[i].date_return is None:
                    if self.bs.check_overdue(self.list[i]) > 0:
                        self.result_table.item(i, j).setBackground(self.__overdue_color)
                    else:
                        self.result_table.item(i, j).setBackground(self.__inactive_color)
                else:
                    self.result_table.item(i, j).setBackground(self.__active_color)

        for i in range(len(self.list), 15):
            for j in range(self.result_table.columnCount()):
                self.result_table.item(i, j).setText("")
                self.result_table.item(i, j).setBackground(self.__active_color)
        self.page_num_label.setText(str(self.page_num) + "/" + str(self.number))
