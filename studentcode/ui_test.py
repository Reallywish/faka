# -*- coding:utf-8 -*-

import tkinter as tk
import threading
from tkinter import messagebox

# 定义全局变量 stop_event
stop_event = threading.Event()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # 创建输入框和按钮，并使用 Grid 布局将其放到左边
        self.input_label = tk.Label(self, text="请输入学信码：")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)
        self.input_text = tk.Text(self, height=40, width=30)
        self.input_text.grid(row=1, column=0, padx=5, pady=5)
        self.submit_button = tk.Button(self, text="提交", command=self.submit)
        self.submit_button.grid(row=2, column=0, padx=5, pady=5)

        # 创建控制台输出框，并使用 Grid 布局将其放到右边
        self.console_frame = tk.Frame(self, bg='black')
        self.console_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.console_text = tk.Text(self.console_frame, bg='black', fg='white')
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_text.config(state=tk.DISABLED)  # 设置只读模式

        # 创建右键菜单
        self.menu = tk.Menu(self.console_text, tearoff=0)
        self.menu.add_command(label="复制", command=self.copy)

        # 将右键菜单绑定到控制台输出框
        self.console_text.bind("<Button-3>", self.show_menu)

        # 设置窗口大小不可调整
        self.master.resizable(0, 0)

        # 监听窗口关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def submit(self):
        # 获取用户输入并输出到控制台
        input_value = self.input_text.get("1.0", tk.END).strip()
        self.console_text.config(state=tk.NORMAL)  # 取消只读模式
        self.console_text.insert(tk.END, f"{input_value}")
        self.console_text.config(state=tk.DISABLED)  # 重新设置只读模式
        # messagebox.showinfo(title="提示", message="已经复制到剪贴板！")

    def show_menu(self, event):
        # 显示右键菜单
        try:
            self.menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.menu.grab_release()

    def copy(self):
        # 复制选中的文本到剪贴板
        selected_text = self.console_text.selection_get()
        self.master.clipboard_clear()
        self.master.clipboard_append(selected_text)

    def on_closing(self):
        # 关闭程序
        stop_event.set()
        self.master.destroy()

if __name__ == "__main__":
    # 创建主窗口对象并启动 GUI 程序
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    # 在后台读取用户输入并输出到控制台
    while not stop_event.is_set():
        input_value = input("请输入命令：")
        print(f"用户命令：{input_value}")
