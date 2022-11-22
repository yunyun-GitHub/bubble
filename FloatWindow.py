from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication, QCursor


class SystemInformation(QWidget):
    def __init__(self):
        super().__init__()
        self.image_size = 180
        self.image = QPixmap('img/bubble.png').scaled(self.image_size, self.image_size, aspectMode=Qt.KeepAspectRatio)
        self.style_sheet = "color: #99FF99; font-size: 17px;"  # background-color:black
        screen = QGuiApplication.primaryScreen().size()  # 获得屏幕的尺寸
        self.position = (screen.width() - 250, screen.height() - 300)  # 移动到右下角位置
        self.main_label_pos = (103, 77)
        self.main_label = None
        self.relative_position = None

        self.create_float_window()  # 创建窗口

    def create_float_window(self):
        """创建浮动窗口"""
        self.resize(self.image.size())  # 设置窗口大小
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)  # 设置无边框和置顶窗口样式隐藏任务栏图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 使透明效果生效
        self.move(self.position[0], self.position[1])  # 调用move移动到右下角位置
        self.main_label = QLabel("", self)
        self.main_label.setAlignment(Qt.AlignRight)  # 右对齐
        self.main_label.setStyleSheet(self.style_sheet)  # 设置样式

    def update_system_information(self, system_information):
        """更新系统信息"""

        # 以右上角为锚点，设置位置，以及内容
        self.main_label.setText(system_information)
        self.main_label.adjustSize()  # Qlabel自适应内容大小
        self.main_label.move(self.main_label_pos[0]-self.main_label.width(), self.main_label_pos[1])

    def mouseDoubleClickEvent(self, event):
        """双击隐藏"""
        self.hide()

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
