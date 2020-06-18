# coding=utf-8
# 软件主窗体
# author: cuihui
import ctypes
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image,ImageTk
import tkinter as tk
from JingDong import JdDetail
from TaoBao import TaobaoDetail
from Analysis import AnalyseBySnow
from DbTools import CommentCloud
import threading
from concurrent.futures import ThreadPoolExecutor
import re
from GUI import MyThread

class Appalication():

    def __init__(self):
        self.comments = []
        window = Tk()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        window.title("CommentsAnalysis")
        window.iconbitmap('logo.ico')
        window.geometry('620x450')
        #window.attributes("-alpha", 0.8)

        # 添加一个多选按钮
        frame1 = Frame(window)
        frame1.pack()  # 包管理器
        self.RbJdTb = IntVar()
        label0 = Label(frame1, text="请选择商品平台")
        rbJd = Radiobutton(frame1, text="京东", variable=self.RbJdTb, value=1)
        rbTb = Radiobutton(frame1, text="淘宝", variable=self.RbJdTb, value=2)
        label0.grid(row=1, column=1)
        rbJd.grid(row=1, column=2)
        rbTb.grid(row=1, column=3)


        frame2 = Frame(window)
        frame2.pack()
        label = Label(frame2, text="请输入商品链接")
        # name = link
        self.name = StringVar()
        entryLink = Entry(frame2, textvariable=self.name, width=50)
        #temp = tk.PhotoImage(file='bgbutton.png')
        btGetComment = Button(frame2, text="获取评论", bg='#99FFC2', command=lambda :self.thread_it(self.processButtonGetComm))
        btCommentAnalyse = Button(frame2, text="评论分析", bg='#CCFFFF', command=self.processButtonCommAna)
        btCommentCloud = Button(frame2, text="生成词云", bg='#DDAAFF', command=self.processButtonCloud)
        label.grid(row=1, column=1)
        entryLink.grid(row=1, column=2)
        btGetComment.grid(row=1, column=3)
        btCommentAnalyse.grid(row=1, column=4)
        btCommentCloud.grid(row=1, column=5)
        frame2.grid_columnconfigure(3, minsize=80)
        frame2.grid_columnconfigure(5, minsize=80)


        frame3 = Frame(window, bg='#C9BBFF')
        frame3.pack()

        lines = []
        with open('test.csv', 'r', encoding='utf-8') as f:
            for i in range(50):
                lines.append(f.readline().strip())
        del(lines[0])
        self.tree = ttk.Treeview(frame3, height=30, show="headings")
        self.tree["columns"] = ("id", "评论内容")
        self.tree.column("id", width=10)
        self.tree.column("评论内容", width=520)
        self.tree.heading("id", text="id")
        self.tree.heading("评论内容", text="评论内容")

        self.tree.pack()

        window.mainloop()


    def processRaidobutton(self):
        if self.RbJdTb.get() == 1:
            print('京东被选中')
        else:
            print('淘宝被选中')
    def setComments(self, comments):
        cnt = 1
        for line in comments:
            if cnt % 2 == 1:
                self.tree.insert("", cnt, text="", values=(cnt, line), tags=('oddrow',))
            else:
                self.tree.insert("", cnt, text="", values=(cnt, line), tags=('evenrow',))
            cnt += 1
        self.tree.tag_configure('oddrow', background='#E4DDFF')
        self.tree.tag_configure('evenrow', background='white')

    #将函数打包进线程
    def thread_it(self, func):
        t = threading.Thread(target=func)
        t.setDaemon(True)
        t.start()

    def callbackJdTb(self, future):
        res = future.result()
        self.comments = res[1]
        self.setComments(self.comments)

    def processButtonGetComm(self):
        if self.RbJdTb.get() == 1:
            link = self.name.get()
            # print(link)
            goodid = re.search('(\d*?).html', link).group(1)
            print(goodid)
            res = JdDetail.getOneGoodComment(goodid, 5)
            self.comments = res[1]
            self.setComments(self.comments)
        elif self.RbJdTb.get() == 2:
            print('Taobao')
            link = self.name.get()
            goodid = re.search('(\d*?)&scene', link).group(1)
            print(goodid)
            self.comments = TaobaoDetail.getComments(goodid)
            self.setComments(self.comments)
        else:
            showinfo('提示', '请选择平台')
    def processButtonCloud(self):
        CommentCloud.create_word_cloud_fq(self.comments)
        top = Toplevel()
        top.geometry('480x480')
        top.title('词云')
        top.iconbitmap('logo.ico')

        canvas_win = tk.Canvas(top, width=480, height=480)
        im = Image.open('wordc.jpg').resize((480, 480))
        im_win = ImageTk.PhotoImage(im)
        canvas_win.create_image(240, 240, image=im_win)
        canvas_win.pack()
        top.mainloop()


    def processButtonCommAna(self):
        # t = MyThread.MyThread(AnalyseBySnow.AnalyseCommentsByList, (self.comments,), 'Ana')
        # t.setDaemon(True)
        # t.start()
        #
        # pos = t.get_result()
        pos = AnalyseBySnow.AnalyseCommentsByList(self.comments)
        top = Toplevel()
        top.geometry('320x240')
        top.title('分析结果')
        top.iconbitmap('logo.ico')

        canvas_win = tk.Canvas(top, width=320, height=240)
        im = Image.open('bgwin.jpg').resize((320, 240))
        im_win = ImageTk.PhotoImage(im)
        canvas_win.create_image(160, 120, image=im_win)
        canvas_win.pack()

        frame = Frame(top)
        frame.pack()
        label = Label(frame, text='共获取到评论%d条\n好评%d条\n差评%d条' %(len(self.comments), pos, len(self.comments)-pos),
                      font=('宋体', 20))
        label.pack()
        canvas_win.create_window(40, 80, anchor=NW, window=frame)

        top.mainloop()
if __name__ == '__main__':
    app = Appalication()