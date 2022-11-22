import sys
from PySide6.QtWidgets import QApplication
from SetUp import SystemTray, SetUp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetUp_window = SetUp()

    bubble_tray = SystemTray(app, SetUp_window)
    bubble_tray.show()

    sys.exit(app.exec())
