import queue
import time
import mss
import cv2
import numpy as np
import pyaudio
import streamlit as st
import yaml
import tkinter as tk
from EmoAIra.forward_module.message_get import message_get
from tkinter import ttk, scrolledtext
import threading
from PIL import Image, ImageTk
from faster_whisper import WhisperModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speech_recognition as sr
import whisper
import sounddevice as sd


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
        st.write("输入的文本为：", text)


def init_ui_tkinter(ch, config):
    #创建主窗口
    root = tk.Tk()
    root.title("emoaira监听入口")

    ###
    # 0.线程模块
    ###


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
            print("无法打开摄像头")
            return
        start_time_pic = time.time() #用于做计时工具
        try:
            while True:
                #（2）实时读取画面
                ret, frame_pic = cap.read()
                if not ret:
                    print("无法读取摄像头画面")
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
            print("摄像头已关闭")
    # 1.3 在一个新线程中运行摄像头更新函数，避免阻塞Tkinter主事件循环
    threading.Thread(target=update_camera, daemon=True).start()
    print('摄像头画面监听已挂起')

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
                print("屏幕监控已关闭")
    # 2.3 在一个新线程中运行屏幕捕获函数，避免阻塞Tkinter主事件循环
    threading.Thread(target=update_screen, daemon=True).start()
    print('屏幕画面监听已挂起')

    # ###
    # # 3.音频接收模块
    # ###
    # # 定义音频参数
    # CHUNK = 1024
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 1
    # RATE = 16000
    #
    # # 创建一个滚动音频监听文本框
    # voice_area = scrolledtext.ScrolledText(root, width=80, height=5, font=("Arial", 12))
    # voice_area.pack(pady=5)
    # # 创建一个Matplotlib图形用于显示音轨
    # fig, ax = plt.subplots()
    # line, = ax.plot(np.zeros(CHUNK))  # 初始化一个零值的音频波形
    # ax.set_ylim(-32768, 32767)  # 设置y轴范围，对应16位音频的范围
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas_widget = canvas.get_tk_widget()
    # canvas_widget.config(width=700, height=50)
    # canvas_widget.pack(pady=5)
    #
    # ##################以下是方法：whisper############################
    # audio_queue = queue.Queue()
    # # 加载 Whisper 模型
    # model = whisper.load_model("tiny")
    # def audio_callback(in_data, frame_count, time_info, status):
    #     """音频回调函数，将音频数据存入队列"""
    #     mic_audio = np.frombuffer(in_data, dtype=np.int16)  # 对应数值
    #     # 更新音轨图像
    #     line.set_ydata(mic_audio)  # 更新音频波形数据
    #     canvas.draw_idle()  # 重绘图形
    #     canvas.flush_events()  # 处理图形事件
    #
    #     audio_queue.put(in_data)
    #     return (in_data, pyaudio.paContinue)
    #
    # def record_audio():
    #     """音频录制线程"""
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
    #                     frames_per_buffer=CHUNK, stream_callback=audio_callback)
    #     stream.start_stream()
    #     #无限循环
    #     while stream.is_active():
    #         pass
    #
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #
    # def process_audio():
    #     """音频处理线程，将音频数据转换为文本;;;;无法识别出，待修改 ！！！！"""
    #     start_time_audio = time.time()
    #     while True:
    #         if not audio_queue.empty() and time.time() - start_time_audio >= config["voice_interval_time"]:
    #             audio_data = audio_queue.get()
    #             # 将音频数据转换为 NumPy 数组
    #             audio_array = np.frombuffer(audio_data, dtype=np.int16)
    #             # 确保 NumPy 数组是可写的
    #             audio_array = np.copy(audio_array)
    #             # 将音频数据转换为浮点型（归一化到 [-1, 1]）
    #             audio_array = audio_array.astype(np.float32) / np.iinfo(np.int16).max
    #             # 使用 Whisper 模型进行语音识别
    #             result = model.transcribe(audio_array)
    #             text = result["text"]
    #             print("Recognized text:", text)
    #             start_time_audio = time.time()
    #
    # # 在一个新线程中运行音频监听函数，避免阻塞 Tkinter 主事件循环
    # threading.Thread(target=record_audio, daemon=True).start()
    # print('音频监听已挂起')
    # threading.Thread(target=process_audio, daemon=True).start()
    # print('音频处理已挂起')


    ###
    # 4.文本读取模块
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
    print('文本输入框监听已挂起')


    # 进入主事件循环
    root.mainloop()
