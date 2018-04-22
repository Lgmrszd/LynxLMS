from PyQt5.QtWidgets import QPushButton, QLayout


def add_button(parent: QLayout, title: str, on_click, width: int = 30, height: int = None) -> QPushButton:
    tr = QPushButton(title)
    tr.setFixedHeight(width)
    if height is not None:
        tr.setFixedHeight(height)
    tr.clicked.connect(on_click)
    parent.addWidget(tr)
    return tr
