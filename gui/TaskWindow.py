from PyQt5.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class Dialog(QMessageBox):
    def __init__(self, name):
        super().__init__()
        self.can_close = False
        self.setWindowTitle(" ")
        label = QLabel(name)
        self.pb = QProgressBar()
        vb = QVBoxLayout()
        vb.addWidget(label, alignment=Qt.AlignCenter)
        vb.addWidget(self.pb)
        self.layout().addLayout(vb, 0, 0)
        self.setStandardButtons(QMessageBox.NoButton)

    def finish(self, message):
        self.can_close = True
        self.close()
        msg = QMessageBox()
        msg.setWindowTitle(" ")
        msg.setText(message)
        msg.exec_()

    def upd(self, pr):
        self.pb.setValue(pr)

    def closeEvent(self, QCloseEvent):
        if self.can_close:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
