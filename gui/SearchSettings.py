from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog, QDialog
from PyQt5.QtCore import Qt


class SearchSettings(QDialog):
    def __init__(self):
        super().__init__()

        window_size_x = 320
        window_size_y = 240
        self.resize(window_size_x, window_size_y)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        sort_label = QLabel("Sort by:")
        self.sortBox = QComboBox()
        self.sortBox.addItems(["Popular", "Name", "New"])

        type_label = QLabel("Show:")
        self.typeBox = QComboBox()
        self.typeBox.addItems(["Book", "Journal", "AV"])

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.close)

        vbox = QVBoxLayout()
        vbox.addWidget(sort_label)
        vbox.addWidget(self.sortBox)
        vbox.addWidget(type_label)
        vbox.addWidget(self.typeBox)
        vbox.addStretch()
        ok_layout = QHBoxLayout()
        ok_layout.addStretch()
        ok_layout.addWidget(ok_button)
        vbox.addLayout(ok_layout)

        self.setLayout(vbox)
        self.setWindowTitle("Search settings")