from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from managers.doc_manager import*


#  !!!Is not ready at all
class CopyEdit(QWidget):
    def __init__(self, copy, on_edit):
        super().__init__()
        self.copy = copy
        self._set_up_ui()
        self._on_edit = on_edit

    def _set_up_ui(self):
        window_size_x = 400
        window_size_y = 400

        vbox = QVBoxLayout()

        self.book_id = QLabel("ID: " + str(self.copy.CopyID))
        top = QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self.book_id)
        vbox.addLayout(top)

        save_button = QPushButton("Save")
        save_button.setFixedWidth(90)
        save_button.setFixedHeight(25)
        save_button.clicked.connect(self.save_changes)

        self.fields = dict()
        self.types = dict()
        dic = {'storage': str, 'checked_out': bool}
        for i in dic:
            line_item = QLineEdit()
            line_item.setText(str(getattr(self.copy, i)))
            self.fields[i] = line_item
            self.types[i] = dic[i]
            line_label = QLabel(str(i) + ':')
            line_label.setFixedWidth(100)
            hbox = QHBoxLayout()
            hbox.addWidget(line_label)
            hbox.addWidget(line_item)
            vbox.addLayout(hbox)
            if dic[i] == bool:
                validator = QIntValidator(0, 1)
                line_item.setValidator(validator)
                line_item.setText(str(int(getattr(self.copy, i))))

        vbox.addStretch()

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(save_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Edit")

    def save_changes(self):
        dic = dict()
        for i in self.fields:
            dic[i] = self.fields[i].text()
        for i in dic:
            if dic[i] == "":
                msg = QMessageBox()
                msg.setText("Empty " + str(i))
                msg.exec_()
                return
        for i in dic:
            setattr(self.copy, i, dic[i])
        self.copy.save()
        self.close()
        self._on_edit()
