from PyQt5.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class Dialog(QMessageBox):
    def __init__(self, name):
        super().__init__()
        self.progress = 0
        label = QLabel(name)
        self.pb = QProgressBar()
        vb = QVBoxLayout()
        vb.addWidget(label, alignment=Qt.AlignCenter)
        vb.addWidget(self.pb)
        self.layout().addLayout(vb, 0, 0)
        self.setStandardButtons(QMessageBox.NoButton)

    def upd(self, pr):
        self.pb.setValue(pr)
        self.progress = pr
        if self.progress == 100:
            self.close()

    def closeEvent(self, QCloseEvent):
        if self.progress < 100:
            QCloseEvent.ignore()
        else:
            QCloseEvent.accept()
