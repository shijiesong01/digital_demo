import threading
import time

from forward_module.action_output import action_output
from forward_module.message_get import message_get
from forward_module.get_input import get_input
from forward_module.input_think import input_think
from forward_module.think_action import think_action

def response_chain(config_data, messagech, response_interval_time, unity_connection):
    is_chain = config_data['is_chain']
    inputch = get_input.InputCh() #创建一个新的结构体
    while is_chain:
        time.sleep(response_interval_time)
        #1.加载配置
        config_get_input = config_data['get_input']
        config_input_think = config_data['input_think']
        config_think_action = config_data['think_action']
        config_action_output = config_data['action_output']
        #2.创建推理结果的存储实例
        inputch.update(config_get_input)
        #3.前向推理
        get_input.Get_input_default(config_get_input, messagech, inputch)
        input_think.Input_think_default(config_input_think, inputch)
        think_action.Think_action_default(config_think_action, inputch)
        action_output.Action_output_default(config_action_output, inputch, unity_connection)


def Chain_test(config_data, unity_connection):
    print('程序启动-----进入执行逻辑chain_test')
    ###
    # 1. 读取配置
    ###
    config_message_get = config_data['message_get']
    config_get_input = config_data['get_input']
    print("----------step2:开始循环链路----------")
    ###
    # 2.创建监听结果的存储实例
    ###
    messagech = message_get.MessageCh(system=config_message_get['system']) #是否开启了监听

    ###
    # 3.同时挂起多个监听线程!
    ###
    message_get.Message_get_default(config_message_get, messagech)


    ###
    # 4.定时，每隔response_interval_time进行一次响应
    ###
    response_interval_time = config_get_input['response_interval_time']
    threading.Thread(target=response_chain, args=(config_data, messagech, response_interval_time, unity_connection), daemon=True).start()



