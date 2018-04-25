from PyQt5.QtWidgets import QPushButton, QLayout
from managers.auth import Auth


def add_button(parent: QLayout, title: str, on_click, cls: str=None, mtd: str=None, width: int=30, height: int=None) -> QPushButton:
    tr = QPushButton(title)
    tr.setFixedHeight(width)
    if height is not None:
        tr.setFixedHeight(height)
    tr.clicked.connect(on_click)
    parent.addWidget(tr)
    if cls is not None and mtd is not None:
        if not Auth.get_access(cls, mtd):
            tr.setEnabled(False)
            tr.setStyleSheet("background-color: grey;")
    return tr
