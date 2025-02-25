###
#本文件中包含了信息接收的所有方法
###
import wave
from datetime import datetime
import threading
import time
import os
import cv2
import pyaudio
import utils
import webrtcvad
import yaml
import speech_recognition as sr
import tkinter as tk

from fontTools.misc.cython import returns

from forward_module.ui.ui_init import *
from forward_module.ui.ui_start import *

###
# 输出（模拟结构体）
# content 内容，任意格式(text文本 pic图像 voice声音 gui界面)
# system 系统状态 on 表示在线 off 表示停止
###
class MessageCh:
    def __init__(self, system='on'):
        self.system = system
        self.content = []
        self.see = ''
    def __getitem__(self):
        return self.content

    # def add(self,content): #添加内容
    #     self.content.append(content)

    def system(self,system): #调整监听通道状态
        self.system = system

###
# 监听text变量的线程函数
# 1. outch[system]不是off时循环进行,off后停止线程
# 2. 监听外部的text变量，不为空时执行：赋值给outch中
###
def listen_text(ch, config, input_text):
    if ch.system != "off": #非off时才监听
        ch.content.append(' ' + input_text)
        print("监听进程-----文本:" + input_text)



def listen_pic(ch, config, pic):
    if ch.system != "off":  # 非off时才监听
        # 确保保存路径存在
        save_path = config['pic_save_path']
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        try:
            # 获取当前时间并格式化为 年-月-日_时-分-秒
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{current_time}.png"
            full_path = f'{save_path}//{file_name}'
            # 保存图片
            pic.save(full_path)
            # 更新当前所见的图像
            ch.see = full_path
            print(f"监听进程-----摄像头:图片已成功保存到 {full_path}")
        except Exception as e:
            print(f"监听进程error-----保存摄像头图片时出现错误: {e}")

def listen_gui(ch, config, gui):
    if ch.system != "off":  # 非off时才监听
        # 确保保存路径存在
        save_path = config['gui_save_path']
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        try:
            # 获取当前时间并格式化为 年-月-日_时-分-秒
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{current_time}.png"
            full_path = os.path.join(save_path, file_name)
            # 保存图片
            gui.save(full_path)
            # 更新当前所见的图像
            ch.see = full_path
            print(f"监听进程-----GUI:图片已成功保存到 {full_path}")
        except Exception as e:
            print(f"监听进程error-----保存gui图片时出现错误: {e}")

# 监听voice变量的线程函数
# ###
# # 3.音频接收模块
# ###
stop_event = threading.Event()
def listen_micro(config):
    # 3.1 初始化VAD,用于切分是否人话
    vad = webrtcvad.Vad()
    # 设置 VAD 灵敏度，值为 1-3，3 最敏感
    vad.set_mode(1)

    # 3.2 设置音频参数并初始化 PyAudio，用于接收音频流
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # RATE 是音频采样率（单位：赫兹）1s内采样次数
    CHUNK = 30  # CHUNK 表示从音频流中一次读取的样本数量（单位：毫秒）
    p = pyaudio.PyAudio()
    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK * RATE // 1000)
    FRAME_DURATION_MS = 30
    SILENCE_THRESHOLD = 40  # 静音帧数阈值
    silence_frames = 0
    is_speaking = False
    audio_frames = []

    # 3.3 不断读取音频流判断并判断是否说话，做语句切分
    while not stop_event.is_set():
        # 读取音频帧
        data = stream.read(CHUNK * RATE // 1000)  # chunk=30指采30个1s的音频（1s内有rate个点），除以1000代表了每个date音频长度是0.03秒
        # 检测当前帧是否为语音
        is_speech = vad.is_speech(data, RATE)
        # print(time.time())
        if is_speech:  # 是语音
            if not is_speaking:  # 如果没开始说话，那么开始
                # 用户开始说话
                is_speaking = True
                print("监听进程-----检测到说话，开始记录...")
            audio_frames.append(data)  # 开始记录音频
            silence_frames = 0
        else:  # 不是语音
            if is_speaking:  # 如果是说话状态
                silence_frames += 1  # 现在没说，因此安静时间+1
                audio_frames.append(data)  # 也记录
                if silence_frames > SILENCE_THRESHOLD:  # 安静太久，视为说完了
                    # 用户停止说话
                    is_speaking = False
                    print("监听进程-----检测到静音，停止记录。")
                    # 调用语音转文本函数
                    # ASR(audio_frames)
                    # 将音频保存为文件
                    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = os.path.join(config['micro_save_path'], current_time)
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(audio_frames))
                    wf.close()
                    print(f"音频已保存为 {filename}")
                    # 清空音频帧，准备下一次记录
                    audio_frames = []



#默认方法
def Message_get_default(config, messagech):
    # 1.开启麦克风监听系统，不在前端显示音轨
    # 创建一个 Event 对象，用于控制线程的运行
    if config["is_micro"]:
        threading.Thread(target=listen_micro, args=(config,), daemon=True).start()
        print('监听进程-----麦克音频监听已挂起')

    # 2.初始化数据库或UI界面
    def run_ui(config, messagech):
        ## 创建文本接收界面
        if config['ui_streamlit'] == True: #还得特定的streamlit run，因此废弃
            ui_start_streamlit(config)
        elif config['ui_tkinter'] == True: #tkinter，包含is_text的文本输入监听
            init_ui_tkinter(messagech, config)
    threading.Thread(target=run_ui, args=(config, messagech), daemon=True).start()


