from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QDialog, QComboBox

class ManageUsersWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 800
        window_size_y = 650

        self.resize(window_size_x, window_size_y)
        self.setWindowTitle('Manage users')