###
#本文件中包含了输入加工的所有方法，不进行大模型推理
###


class InputCh:
    def __init__(self):
        self.content = {}

    def __getitem__(self):
        return self.content

    def __setitem__(self, key, value):
        self.content[key] = value


def extract_and_format(content, memory_length):
    ###
    # 此函数用于将message.content中的监听信息进行指定规则的截取
    ##
    # 找到倒数第二个'text'的索引
    text_indices = [i for i, item in enumerate(content) if item.startswith('text')]
    if len(text_indices) < memory_length:
        extracted_content = content
    else:
        start_index = text_indices[-memory_length]
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
    ###
    #stpe1.提取messagech模块
    ###
    inputch.content['talk'] = extract_and_format(messagech.content, memory_length=config['memory_length'])
    #提取后删除messagech板块的历史内容
    messagech.content = []

    ###
    #step2.记忆加载模块
    ###
    inputch.content['long_history'] = ''
    inputch.content['short_history'] = ''

    ###
    #step3.性格调取模块
    ###
    inputch.content['mood'] = '积极向上，有更深的探索欲望'


