import sys
import time
import psutil
from PySide6.QtCore import Qt, QThread, Signal, QCoreApplication
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QSystemTrayIcon, QMenu
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication, QCursor, QIcon, QAction


class UpdateSystemInformation(QThread):
    def __init__(self, signal):
        super().__init__()
        self.main_thread_update_system_information_signal = signal

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

            self.main_thread_update_system_information_signal.emit(f"{sent} ↑\n{recv} ↓")

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
    update_system_information_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.image_size = 180
        self.image = QPixmap('img/bubble.png').scaled(self.image_size, self.image_size, aspectMode=Qt.KeepAspectRatio)
        self.default_label = None
        self.relative_position = None

        self.create_float_window()
        self.update_system_information_signal.connect(self.update_system_information)
        self.update_system_information_thread = UpdateSystemInformation(self.update_system_information_signal)
        self.update_system_information_thread.start()

    def create_float_window(self):
        """创建浮动窗口"""
        self.resize(self.image.size())  # 设置窗口大小
        # self.setMask(self.image.mask())  # 设置遮罩
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)  # 设置无边框和置顶窗口样式隐藏任务栏图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 使透明效果生效
        screen = QGuiApplication.primaryScreen().size()  # 获得屏幕的尺寸
        self.move(screen.width() - 250, screen.height() - 300)  # 调用move移动到右下角位置
        self.default_label = QLabel("This is a placeholder text", self)
        self.default_label.setGeometry(30, 85, 68, 26)
        self.default_label.setStyleSheet("color: #99FF99; ")

    def update_system_information(self, x):
        self.default_label.setText(x)

    def mouseDoubleClickEvent(self, event):
        """双击退出"""
        # app.quit()
        self.hide()

    def closeEvent(self, event):
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


def quit_app():
    float_window.show()
    QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # QApplication.setQuitOnLastWindowClosed(False)
    float_window = FloatWindow()
    float_window.show()

    tp = QSystemTrayIcon(float_window)
    tp.setIcon(QIcon('img/bubble.png'))
    a1 = QAction('&显示(Show)', triggered=float_window.show)
    a2 = QAction('&退出(Exit)', triggered=quit_app)  # 直接退出可以用qApp.quit
    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    sys.exit(app.exec())
