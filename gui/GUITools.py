from PyQt5.QtWidgets import QPushButton, QLayout


def add_button(parent: QLayout, title: str, on_click: callable, width: int = 30) -> QPushButton:
    tr = QPushButton(title)
    tr.setFixedHeight(width)
    tr.clicked.connect(on_click)
    parent.addWidget(tr)
    return tr
