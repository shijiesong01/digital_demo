import threading
import time

from forward_module.action_output.action_output import *
from forward_module.message_get.message_get import *
from forward_module.get_input.get_input import *
from forward_module.input_action.input_action import *

def response_chain(config_data, messagech, response_interval_time, unity_connection):
    is_chain = config_data['is_chain']
    inputch = InputCh() #创建一个新的结构体
    while is_chain:
        time.sleep(response_interval_time)
        #1.加载配置
        config_get_input = config_data['get_input']
        config_input_action = config_data['input_action']
        config_action_output = config_data['action_output']
        #2.创建推理结果的存储实例
        inputch.update(config_get_input)
        #3.前向推理
        Get_input_default(config_get_input, messagech, inputch)
        Input_action_default(config_input_action, inputch)
        Action_output_default(config_action_output, inputch, unity_connection)


def Chain_llm(config_data, unity_connection):
    print('程序启动-----进入执行逻辑chain_llm')
    ###
    # 1. 读取配置
    ###
    config_message_get = config_data['message_get']
    config_get_input = config_data['get_input']
    print("----------step2:开始循环链路----------")
    ###
    # 2.创建监听结果的存储实例
    ###
    messagech = MessageCh(system=config_message_get['system']) #是否开启了监听

    ###
    # 3.同时挂起多个监听线程!
    ###
    Message_get_default(config_message_get, messagech)


    ###
    # 4.定时，每隔response_interval_time进行一次响应
    ###
    response_interval_time = config_get_input['response_interval_time']
    threading.Thread(target=response_chain, args=(config_data, messagech, response_interval_time, unity_connection), daemon=True).start()



