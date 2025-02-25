###
# 测试音频接受部分
###

import pyaudio
import wave
import speech_recognition as sr
import webrtcvad
import time

# 初始化 VAD
vad = webrtcvad.Vad()
# 设置 VAD 灵敏度，值为 1-3，3 最敏感
vad.set_mode(1)

# 音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 #RATE 是音频采样率（单位：赫兹）1s内采样次数
CHUNK = 30 #CHUNK 表示从音频流中一次读取的样本数量（单位：毫秒）
FRAME_DURATION_MS = 30
SILENCE_THRESHOLD = 40  # 静音帧数阈值

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK * RATE // 1000)

print("开始监听...")

silence_frames = 0
is_speaking = False
audio_frames = []

# 定义语音转文本函数
def ASR(audio_frames):
    # 保存音频数据
    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

    # 语音转文本
    r = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='zh-CN')
        print(f"识别结果: {text}")
        # 这里可以添加反馈逻辑，例如简单打印反馈信息
        print("已收到你的话，正在处理...")
    except sr.UnknownValueError:
        print("无法识别语音")
    except sr.RequestError as e:
        print(f"请求错误; {e}")

try:
    while True:
        # 读取音频帧
        data = stream.read(CHUNK * RATE // 1000) #chunk=30指采30个1s的音频（1s内有rate个点），除以1000代表了每个date音频长度是0.03秒
        # 检测当前帧是否为语音
        is_speech = vad.is_speech(data, RATE)
        #print(time.time())
        if is_speech: #是语音
            if not is_speaking: #如果没开始说话，那么开始
                # 用户开始说话
                is_speaking = True
                print("监听进程-----检测到说话，开始记录...")
            audio_frames.append(data) #开始记录音频
            silence_frames = 0
        else: #不是语音
            if is_speaking: #如果是说话状态
                silence_frames += 1 # 现在没说，因此安静时间+1
                audio_frames.append(data) #也记录
                if silence_frames > SILENCE_THRESHOLD: #安静太久，视为说完了
                    # 用户停止说话
                    is_speaking = False
                    print("监听进程-----检测到静音，停止记录。")
                    # 调用语音转文本函数
                    #ASR(audio_frames)
                    # 将音频保存为文件
                    filename = f"../../log/history/message_get/micro/{int(time.time())}.wav"
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(audio_frames))
                    wf.close()
                    print(f"音频已保存为 {filename}")

                    # 清空音频帧，准备下一次记录
                    audio_frames = []
except KeyboardInterrupt:
    print("程序终止，正在清理资源...")
finally:
    # 停止音频流
    stream.stop_stream()
    # 关闭音频流
    stream.close()
    # 终止 PyAudio 对象
    p.terminate()