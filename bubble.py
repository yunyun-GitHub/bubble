import sys
import time
import psutil
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QSystemTrayIcon, QMenu
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication, QCursor, QIcon, QAction


class BubbleTray(QSystemTrayIcon):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setIcon(QIcon('img/bubble.png'))
        # self.setVisible(True)  # 没有这一句不会显示系统托盘

        # Create the menu
        self.menu = QMenu()

        self.menu_more = QMenu("更多(more)")
        self.action_fun1 = QAction('功能1(fun1)')
        self.menu_more.addAction(self.action_fun1)
        self.action_fun2 = QAction('功能2(fun2)')
        self.menu_more.addAction(self.action_fun2)
        self.menu.addMenu(self.menu_more)

        self.action_show = QAction('显示(Show)', triggered=self.window.show)
        self.menu.addAction(self.action_show)
        self.action_exit = QAction('退出(Exit)', triggered=self.all_quit)
        self.menu.addAction(self.action_exit)

        # Add the menu to the tray
        self.setContextMenu(self.menu)

    def all_quit(self):
        self.window.close()
        app.quit()


class SystemInformation(QThread):
    system_information_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        while True:
            time.sleep(1)
            sent_now = psutil.net_io_counters().bytes_sent
            recv_now = psutil.net_io_counters().bytes_recv

            # 算出1秒后的差值,并转换
            sent = self.conversion(sent_now - sent_before)
            recv = self.conversion(recv_now - recv_before)

            sent_before = sent_now
            recv_before = recv_now

            self.system_information_signal.emit(f"{sent} ↑\n{recv} ↓")

    @staticmethod
    def conversion(bit):
        if bit < 1024:
            speed = '%sB/s' % bit
        elif bit < 1048576:
            speed = '%sK/s' % round(bit / 1024, 2)
        else:
            speed = '%sM/s' % round(bit / 1048576, 2)
        return speed.rjust(10, ' ')


class FloatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.image_size = 180
        self.image = QPixmap('img/bubble.png').scaled(self.image_size, self.image_size, aspectMode=Qt.KeepAspectRatio)
        self.default_label = None
        self.relative_position = None

        self.create_float_window()  # 创建窗口

        # 启动子线程
        self.update_system_information_thread = SystemInformation()
        self.update_system_information_thread.system_information_signal.connect(self.update_system_information)
        self.update_system_information_thread.start()

    def create_float_window(self):
        """创建浮动窗口"""
        self.resize(self.image.size())  # 设置窗口大小
        # self.setMask(self.image.mask())  # 设置遮罩
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)  # 设置无边框和置顶窗口样式隐藏任务栏图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 使透明效果生效
        screen = QGuiApplication.primaryScreen().size()  # 获得屏幕的尺寸
        self.move(screen.width() - 250, screen.height() - 300)  # 调用move移动到右下角位置
        self.default_label = QLabel("0000.00B/s ↑\n0000.00B/s ↓", self)
        self.default_label.setAlignment(Qt.AlignRight)
        self.default_label.setStyleSheet("color: #99FF99; font-size: 17px")  # background-color:black
        # self.default_label.setGeometry(10, 77, 80, 29)
        self.default_label.move(-5, 77)

    def update_system_information(self, system_information):
        self.default_label.setText(system_information)

    def mouseDoubleClickEvent(self, event):
        """双击隐藏"""
        self.hide()

    def closeEvent(self, event):
        # print("进入closeEvent")
        self.update_system_information_thread.terminate()  # 结束此线程
        self.update_system_information_thread.wait()  # 等待结束完成
        if self.update_system_information_thread.isFinished():  # 如果当前线程已经完成工作，则删除
            del self.update_system_information_thread

    def paintEvent(self, event):
        """绘制窗口"""
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.image.width(), self.image.height(), self.image)

    def mousePressEvent(self, event):
        """左键按下"""
        self.relative_position = QCursor.pos() - self.pos()

    def mouseMoveEvent(self, event):
        """左键移动"""
        self.move(QCursor.pos() - self.relative_position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)
    float_window = FloatWindow()
    float_window.show()

    bubble_tray = BubbleTray(float_window)
    bubble_tray.show()

    sys.exit(app.exec())
