import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory

import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    main_window = MainWindow.MainWindow()
    main_window.show()

    sys.exit(app.exec_())