import queue
import time
import mss
import cv2
import numpy as np
import pyaudio
import streamlit as st
import yaml
import tkinter as tk
from forward_module.message_get import message_get
import threading
from PIL import Image, ImageTk
import time

###
# 因streamlit特殊的启动方式较为复杂，因此暂时废弃streamlit作为ui前端
###
#if __name__ == "__main__":
def init_ui_streamlit():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    # 创建输入框
    text_input = st.text_input("请输入文本：", key="text_input")
    # 创建发送按钮
    if st.button("发送"):
        # 获取输入框的文本
        text = st.session_state.text_input
        # 显示获取的文本
        st.write("监听进程-----输入的文本为：", text)


def init_ui_tkinter(ch, config):
    #创建主窗口
    root = tk.Tk()
    root.title("emoaira监听入口")

    ###
    # 1.摄像头读取模块
    ###
    # 1.1 创建一个标签用于显示摄像头画面
    pic_window_width = config['pic_window_width']
    pic_window_height = config['pic_window_height']
    label_pic = tk.Label(root,width=pic_window_width,height=pic_window_height) #18:13/720:520/900:650
    label_pic.pack(pady=5)
    # 1.2 定义一个函数用于更新摄像头画面
    def update_camera():
        # （1）打开摄像头
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("监听进程error-----无法打开摄像头")
            return
        start_time_pic = time.time() #用于做计时工具
        try:
            while True:
                #（2）实时读取画面
                ret, frame_pic = cap.read()
                if not ret:
                    print("监听进程error-----无法读取摄像头画面")
                    break

                #（3）将画面展示到前端
                frame_pic = cv2.cvtColor(frame_pic, cv2.COLOR_BGR2RGB) #将摄像头画面转换为Tkinter可以显示的格式
                im_pic = Image.fromarray(frame_pic) #画面图像<PIL.Image.Image image mode=RGB size=640x480 at 0x2619E7AD810>
                # 更新前端展示的标签的内容
                im_pic_resized = im_pic.resize((pic_window_width,pic_window_height))  # 调整图像大小以适应Label
                img_pic_resized = ImageTk.PhotoImage(image=im_pic_resized)
                label_pic.config(image=img_pic_resized)
                label_pic.image = img_pic_resized  # 保持对PhotoImage的引用

                #（4）每隔一段时间将画面作为监听信息存入
                if config["is_pic"]:
                    if time.time() - start_time_pic >= config["pic_interval_time"]:
                        message_get.listen_pic(ch, config, im_pic)
                        start_time_pic = time.time()
                # 每次更新后让Tkinter处理其他事件
                root.update()
        finally:
            # （5）释放摄像头资源
            cap.release()
            print("监听进程-----摄像头已关闭")
    # 1.3 在一个新线程中运行摄像头更新函数，避免阻塞Tkinter主事件循环
    threading.Thread(target=update_camera, daemon=True).start()
    print('监听进程-----摄像头画面监听已挂起')

    ###
    # 2.屏幕界面读取模块
    ###
    # 2.1 创建一个标签用于显示屏幕画面
    gui_window_width = config['gui_window_width']
    gui_window_height = config['gui_window_height']
    label_gui = tk.Label(root,width=gui_window_width,height=gui_window_height)
    label_gui.pack(pady=5)
    # 2.2 定义一个函数用于更新屏幕画面
    def update_screen():
        # （1）截取屏幕
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 2550, "height": 1400} #上左距离（0,0），截图宽高（）
            start_time_gui = time.time()  # 用于做计时工具
            try:
                while True:
                    # （2）实时读取屏幕
                    frame_gui = np.array(sct.grab(monitor))

                    # （3）将画面展示到前端
                    frame_gui = cv2.cvtColor(frame_gui, cv2.COLOR_BGRA2RGB) # 将摄像头画面转换为Tkinter可以显示的格式
                    im_gui = Image.fromarray(frame_gui)
                    # 更新前端展示的标签的内容
                    im_gui_resized = im_gui.resize((gui_window_width,gui_window_height))  # 调整图像大小以适应Label
                    img_gui_resized = ImageTk.PhotoImage(image=im_gui_resized)
                    label_gui.config(image=img_gui_resized)
                    label_gui.image = img_gui_resized

                    # （4）每隔一段时间将画面作为监听信息存入
                    if config["is_gui"]:
                        if time.time() - start_time_gui >= config["gui_interval_time"]:
                            message_get.listen_gui(ch, config, im_gui)
                            start_time_gui = time.time()
                    root.update()
            finally:
                # （5）释放资源
                sct.close()
                print("监听进程-----屏幕监控已关闭")
    # 2.3 在一个新线程中运行屏幕捕获函数，避免阻塞Tkinter主事件循环
    threading.Thread(target=update_screen, daemon=True).start()
    print('监听进程-----屏幕画面监听已挂起')


    ###
    # 3.文本读取模块
    ###
    #创建输入框
    entry = tk.Entry(root, width=100)
    entry.pack(pady=5) #添加并设置垂直方向的外边距为10像素

    # 创建按钮，点击按钮时将输入框内容传入listen_text函数
    def on_button_click():
        #当监听文本信息时，会触发message_get.listen_text；否则按按钮会没反应
        if config["is_text"]:
            input_text = entry.get()
            message_get.listen_text(ch, config,input_text)
    button = tk.Button(root, text="提交", command=on_button_click)
    button.pack(pady=10)
    print('监听进程-----文本输入框监听已挂起')


    # 进入主事件循环
    root.mainloop()
