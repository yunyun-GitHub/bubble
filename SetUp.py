import random
import time
import psutil
from FloatWindow import SystemInformation
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QCursor, QIcon, QAction, QPalette, QColor
from PySide6.QtWidgets import QWidget, QSystemTrayIcon, QMenu, QLabel, QListWidgetItem, QPushButton, QHBoxLayout, \
    QSpacerItem, QSizePolicy

from ui.SetUp import Ui_SetUp


class SetUp(QWidget, Ui_SetUp):
    broadcast_to_child_threads_signal = Signal(str)
    interface_deleteFloatWindow_signal = Signal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 载入主窗口UI界面
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)  # 设置无边框和置顶窗口样式隐藏任务栏图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 使透明效果生效
        self.relative_position = None

        # 启动子窗口
        self.bubble_window = SystemInformation()
        self.bubble_window.show()

        # 启动子线程
        self.update_system_information_thread = InformationThread(self.broadcast_to_child_threads_signal)
        self.update_system_information_thread.start()

        # 连接信号与槽
        self.addButton.clicked.connect(self.addFloatWindow)  # 点击添加窗口项
        self.ListWidgetFloatWindow.itemClicked.connect(self.item_clicked)  # 窗口项点击处理
        self.interface_deleteFloatWindow_signal.connect(self.deleteFloatWindow)  # 删除小窗口项
        self.hideButton.clicked.connect(self.hide)  # 点击右上角X，隐藏主界面
        self.update_system_information_thread.system_information_signal.connect(
            self.bubble_window.update_system_information)  # 子线程与子窗口

    def item_clicked(self, item):
        """点击窗口项显示该窗口"""
        self.stackedWidget.setCurrentWidget(item.stacked_widget)

    def addFloatWindow(self):
        """添加窗口项"""
        color_list = ["red", "green", "yellow", "blue"]
        color = random.choice(color_list)

        item = QListWidgetItem()
        item.stacked_widget = Color(color)  # 将StackedWidget和ListWidget绑定

        # 添加StackedWidget页
        self.stackedWidget.addWidget(item.stacked_widget)
        # 添加ListWidget项
        self.ListWidgetFloatWindow.addItem(item)
        widget = CustomizeWidget(color, item, self.interface_deleteFloatWindow_signal)
        self.ListWidgetFloatWindow.setItemWidget(item, widget)

        self.stackedWidget.setCurrentWidget(item.stacked_widget)  # 添加之后自动显示

    def deleteFloatWindow(self, item):
        """删除窗口项"""
        self.stackedWidget.removeWidget(item.stacked_widget)
        self.ListWidgetFloatWindow.takeItem(self.ListWidgetFloatWindow.row(item))

    def closeEvent(self, event):
        self.broadcast_to_child_threads_signal.emit("exit")

    def mousePressEvent(self, event):
        """左键按下"""
        self.relative_position = QCursor.pos() - self.pos()

    def mouseMoveEvent(self, event):
        """左键移动"""
        self.move(QCursor.pos() - self.relative_position)


class InformationThread(QThread):
    system_information_signal = Signal(str)

    def __init__(self, parent_thread_signal):
        super().__init__()
        self.parent_thread_signal = parent_thread_signal

        self.parent_thread_signal.connect(self.parent_thread_signal_processing)

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
        return speed

    def parent_thread_signal_processing(self, signal):
        if signal == "exit":
            self.terminate()
            self.wait()  # 等待结束完成


class SystemTray(QSystemTrayIcon):
    def __init__(self, myapp, window):
        super().__init__()
        self.app = myapp
        self.window = window
        self.setIcon(QIcon('img/bubble.png'))
        self.activated.connect(self.iconClicked)

        # Create the menu
        self.menu = QMenu()
        self.menu_more = QMenu("更多(more)")
        self.action_fun1 = QAction('功能1(fun1)')
        self.menu_more.addAction(self.action_fun1)
        self.action_fun2 = QAction('功能2(fun2)')
        self.menu_more.addAction(self.action_fun2)
        self.menu.addMenu(self.menu_more)
        self.action_exit = QAction('退出(Exit)', triggered=self.all_quit)
        self.menu.addAction(self.action_exit)

        # 设置右键单击
        self.setContextMenu(self.menu)

    def iconClicked(self, reason):
        """
        ActivationReason.Trigger  左键单击
        ActivationReason.DoubleClick  左键双击
        ActivationReason.Context  右键单击
        """
        if reason == self.ActivationReason.DoubleClick:  # 双击
            self.window.show()

    def all_quit(self):
        self.window.close()
        self.app.quit()


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class CustomizeWidget(QWidget):

    def __init__(self, color, item, delete_signal):
        super().__init__()
        self.item = item
        self.delete_signal = delete_signal

        layout = QHBoxLayout()
        label = QLabel(color)
        layout.addWidget(label)

        layout.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        button = QPushButton("X")
        button.clicked.connect(self.buttonClicked)  # 连接点击槽
        layout.addWidget(button)

        self.setLayout(layout)

    def buttonClicked(self):
        self.delete_signal.emit(self.item)
