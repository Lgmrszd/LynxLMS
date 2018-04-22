from PyQt5.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._set_up_ui()

    def _set_up_ui(self):
        pass

    def compare_window(self, param: dict) -> bool:
        return True

    def closeEvent(self, QCloseEvent):
        super(Window, self).closeEvent(QCloseEvent)
        self.app.forget_window(self)
        pass
