###
#本文件中包含了输入加工的所有方法，不进行大模型推理
###
import threading

from EmoAIra.backstage_module.character_update import character
from EmoAIra.backstage_module.memory_update import memory

class InputCh:
    def __init__(self):
        self.last_content = [] #短期记忆
        self.content = {'long_memory':'', 'short_memory':''} #本轮对话
        self.response_num = 0 #统计对话轮数

    def __getitem__(self):
        return self.content

    def __setitem__(self, key, value):
        self.content[key] = value

    def update(self, config):
        self.last_content.append(self.content) #内容更新
        self.content = {'long_memory':self.last_content[-1]['long_memory'], 'short_memory':memory.short_memory_update(config, self.last_content)}
        self.response_num += 1 #对话轮数增加

        # 达到某对话轮数后，启一个进程自动更新长期记忆
        if self.response_num % config['long_memory_update_num'] == 0:
            threading.Thread(target=memory.long_memory_update, args=(config, self),daemon=True).start()

        # 记忆长度超过某对话轮数后，记忆滚动
        if len(self.last_content) > config['long_memory_update_num']:
            self.last_content = self.last_content[1:]  # 除去最前一轮


def extract_and_format(content, get_length):
    ###
    # 此函数用于将message.content中的监听信息进行指定规则的截取
    ##
    # 找到倒数第二个'text'的索引
    text_indices = [i for i, item in enumerate(content) if item.startswith('text')]
    if len(text_indices) < get_length:
        extracted_content = content
    else:
        start_index = text_indices[-get_length]
        # 提取从倒数第二个'text'开始到最后的内容
        extracted_content = content[start_index:]
    # 格式化内容
    formatted_content = []
    for item in extracted_content:
        if item:
            formatted_content.append(item)
    # 将格式化后的内容拼接成字符串
    result = '\n'.join(formatted_content)
    return result

#默认方法
def Get_input_default(config, messagech, inputch):
    print('-----step3.1:输入梳理模块-----')
    print('监听信息:', messagech.content)

    if inputch.last_content != []:
        feel = inputch.last_content[-1]['feel'] #加载上一轮的感受，指导本轮的性格

    else:
        feel = ''

    ###
    #stpe1.提取messagech模块
    ###
    inputch.content['talk'] = extract_and_format(messagech.content, get_length=config['get_length'])
    #提取后删除messagech板块的历史内容
    messagech.content = []

    ###
    #step2.记忆加载模块
    ###
    # 已在update()中更新

    ###
    #step3.性格调取模块
    ###
    inputch.content['mood'] = character.update_Character(config, feel)


