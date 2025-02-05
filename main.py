import time
import yaml
from chain import chain_test,chain_llm



if __name__ == '__main__':
    ###
    # 1. 读取配置
    ###
    # 打开并读取YAML文件
    print("------------------------------------------\nstep1:准备初始化")
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    print('成功读取yaml')
    ###
    # 2.获取链路名称并执行对应的链路
    ###
    chain_name = config_data['main']['chain']
    if chain_name == "chain_test":
        chain_test.Chain_test(config_data)
    elif chain_name == "chain_llm":
        chain_llm.Chain_llm(config_data)

    ###
    # 3.无限循环确保进程的进行
    ###
    try:
        while True:
            time.sleep(10)  # 服务主循环休眠，避免过度占用CPU
            #print(messagech.content)
    except KeyboardInterrupt:
        print("Service stopped by user.")







