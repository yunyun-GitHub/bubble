import tkinter
import threading
import pystray
import time
import psutil
from PIL import ImageTk, Image


class FloatWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.image_h = 80
        self.image = self.image_resize("img/写字板.png")
        self.tray = pystray.Icon("tray", self.image, "鼠标移动到\n托盘图标上\n展示内容", menu=pystray.Menu(
            pystray.MenuItem("更多", pystray.Menu(
                pystray.MenuItem("广告招商中", self.on_clicked),
                pystray.MenuItem("广告招商中", self.on_clicked),
            )),
            pystray.MenuItem("广告招商中", self.on_clicked),
            pystray.MenuItem(text='唤醒窗口', action=self.on_clicked, default=True, visible=False),
            pystray.MenuItem("退出", self.on_clicked),
        ))

        self.X = self.Y = 0
        self.geometry(f'{self.image.size[0]}x{self.image.size[1]}-100-200')  # 设置窗口大小适应图片
        self.overrideredirect(True)  # 去除标题栏
        self.wm_attributes('-transparentcolor', 'gray')  # 设置窗口透明
        # self.wm_attributes("-alpha", 0.5)  # 透明度(0.0~1.0)
        self.wm_attributes("-topmost", True)  # 永远处于顶层

        image = ImageTk.PhotoImage(self.image)
        self.lbimage = tkinter.Label(self, image=image, bd=0, bg='gray', text="", compound=tkinter.CENTER)
        self.lbimage.image = image
        self.lbimage.place(x=0, y=0)
        self.lbimage.bind("<Button-1>", self.mousedown)  # 鼠标按下绑定函数，决定可以移动窗体
        self.lbimage.bind("<Double-Button-1>", self.hide_window)  # 双击退出
        self.lbimage.bind("<B1-Motion>", self.mousemove)  # 鼠标按下并移动绑定函数，决定窗体移动到新的位置

        threading.Thread(target=self.tray.run, daemon=True).start()
        threading.Thread(target=self.update_text, daemon=True).start()

    def update_text(self):
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

            self.lbimage.config(text=f"{sent} ↑\n{recv} ↓")

    @staticmethod
    def conversion(bit):
        if bit < 1024:
            speed = '%sB/s' % bit
        elif bit < 1048576:
            speed = '%sK/s' % round(bit / 1024, 2)
        else:
            speed = '%sM/s' % round(bit / 1048576, 2)
        return speed.rjust(10, ' ')

    def image_resize(self, image_path):
        img = Image.open(image_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        w = int(img.size[0] * self.image_h / img.size[1])
        return img.resize((w, self.image_h))

    def mousedown(self, event):  # 获取鼠标相对于窗体的坐标
        self.X, self.Y = event.x, event.y

    def mousemove(self, event):
        self.geometry(f'+{event.x_root - self.X}+{event.y_root - self.Y}')

    def hide_window(self, event):
        self.withdraw()
        return event

    def on_clicked(self, icon, item):
        if str(item) == "广告招商中":
            print("广告招商中")
        elif str(item) == "唤醒窗口":
            self.deiconify()
        elif str(item) == "退出":
            icon.stop()
            self.destroy()


float_window = FloatWindow()
float_window.mainloop()
