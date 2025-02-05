###
#本文件中包含了信息接收的所有方法
###
import threading
import time

import cv2
import utils
import yaml
import speech_recognition as sr
import tkinter as tk
from EmoAIra.forward_module.message_get import get_text,get_pic,get_voice,get_gui
from EmoAIra.forward_module.ui import ui_start,ui_init

###
# 输出（模拟结构体）
# content 内容，任意格式(text文本 pic图像 voice声音 gui界面)
# system 系统状态 on 表示在线 off 表示停止
###
class MessageCh:
    def __init__(self, system='on'):
        self.system = system
        self.content = []

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
        ch.content.append('text: ' + input_text)
        print("Message_get->Text thread processed,", 'text: ' + input_text)

# 监听pic变量的线程函数
def listen_pic(ch, config, pic):
    #pic.show()
    if ch.system != "off": #非off时才监听
        # ch.content.append('pic: ' + pic)
        # print("Message_get->Pic thread processed,", 'pic: ' + pic)
        pass


# 监听voice变量的线程函数
def listen_voice(audio_data,voice_area,config):
    # 初始化识别器
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data, language='zh-CN')
        print('text',text)
        if text.strip():
            voice_area.insert(tk.END, f"麦克风：{text}\n")
            voice_area.see(tk.END)  # 自动滚动到底部
    except sr.UnknownValueError:
        print("无法识别语音")
    except sr.RequestError as e:
        print(f"请求错误：{e}")

def listen_gui(ch, config, gui):
    #gui.show()
    if ch.system != "off": #非off时才监听
        # ch.content.append('gui: ' + gui)
        # print("Message_get->Gui thread processed,", 'gui: ' + gui)
        pass

#默认方法
def Message_get_default(config, messagech):

    # 1.初始化数据库或UI界面
    def run_ui(config, messagech):
        ## 创建文本接收界面
        if config['ui_streamlit'] == True: #还得特定的streamlit run，因此废弃
            ui_start.ui_start_streamlit(config)
        elif config['ui_tkinter'] == True: #tkinter，包含is_text的文本输入监听
            ui_init.init_ui_tkinter(messagech, config)
    threading.Thread(target=run_ui, args=(config, messagech), daemon=True).start()


