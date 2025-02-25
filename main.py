import os
import time
import yaml
from chain import chain_test,chain_llm
from forward_module.action_output.live2d import *


if __name__ == '__main__':
    ###
    # 1.读取配置
    ###
    # 打开并读取YAML文件
    print("----------step1:开始初始化----------")
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    print('程序启动-----成功读取yaml')

    ###
    # 2.初始化输出系统
    ###
    if config_data['main']['live2d_unity_system']:
        # 触发 live2unity 函数
        unity_connection = live2d_unity_init()
        print('程序启动-----成功启动live2d—unity')
    else:
        unity_connection = None
    ###
    # 3.log日志初始化
    ###
    # 判断是否清空历史摄像头记忆
    if config_data['main']['clear_log_history_pic']:
        pic_file_path = config_data['message_get']['pic_save_path']
        # 检查路径是否存在
        if os.path.exists(pic_file_path):
            # 遍历指定路径下的所有文件和文件夹
            for root, dirs, files in os.walk(pic_file_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    try:
                        # 删除文件
                        os.remove(file_full_path)
                    except Exception as e:
                        print(f"删除文件 {file_full_path} 时出错: {e}")
                print(f"程序启动-----已清空 {pic_file_path}路径下所有历史摄像头图片")
        else:
            print(f"程序启动error-----指定的路径 {pic_file_path} 不存在。")
    # 判断是否清空历史GUI图像记忆
    if config_data['main']['clear_log_history_gui']:
        gui_file_path = config_data['message_get']['gui_save_path']
        # 检查路径是否存在
        if os.path.exists(gui_file_path):
            # 遍历指定路径下的所有文件和文件夹
            for root, dirs, files in os.walk(gui_file_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    try:
                        # 删除文件
                        os.remove(file_full_path)
                    except Exception as e:
                        print(f"删除文件 {file_full_path} 时出错: {e}")
                print(f"程序启动-----已清空 {gui_file_path}路径下所有历史摄像头图片")
        else:
            print(f"程序启动error-----指定的路径 {gui_file_path} 不存在。")
    # 判断是否清空历史麦克风记忆
    if config_data['main']['clear_log_history_micro']:
        micro_file_path = config_data['message_get']['micro_save_path']
        # 检查路径是否存在
        if os.path.exists(micro_file_path):
            # 遍历指定路径下的所有文件和文件夹
            for root, dirs, files in os.walk(micro_file_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    try:
                        # 删除文件
                        os.remove(file_full_path)
                    except Exception as e:
                        print(f"删除文件 {file_full_path} 时出错: {e}")
                print(f"程序启动-----已清空 {micro_file_path}路径下所有历史麦克风音频")
        else:
            print(f"程序启动error-----指定的路径 {micro_file_path} 不存在。")
    ###
    # 4.获取链路名称并执行对应的链路
    ###
    chain_name = config_data['main']['chain']
    if chain_name == "chain_test":
        chain_test.Chain_test(config_data, unity_connection)
    elif chain_name == "chain_llm":
        chain_llm.Chain_llm(config_data,unity_connection)

    ###
    # 5.无限循环确保进程的进行
    ###
    try:
        while True:
            time.sleep(10)  # 服务主循环休眠，避免过度占用CPU
            #print(messagech.content)
    except KeyboardInterrupt:
        print("程序结束-----Service stopped by user.")







