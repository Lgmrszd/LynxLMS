from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QGroupBox


class UserInfo(QWidget):
    def __init__(self, userObj):
        super().__init__()
        self.userObj = userObj
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        self.user_id = QLabel("ID: " + str(self.userObj.card_id))

        self.history_table = QTableWidget()

        self.history_table.doubleClicked.connect(self.cell_clicked_event)

        vbox = QVBoxLayout()

        id_layout = QHBoxLayout()
        id_layout.addStretch()
        id_layout.addWidget(self.user_id)

        history_table_group = QGroupBox()
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.history_table)
        history_table_group.setLayout(table_layout)

        vbox.addLayout(id_layout)
        vbox.addWidget(history_table_group)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle(self.userObj.name + " " + self.userObj.surname + " information")

    def cell_clicked_event(self):
        pass