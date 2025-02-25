from src.prompt.template import *
from src.llm.llm_api import *


def short_memory_update(config, last_content):
    short_memory_length = config['short_memory_length']
    filtered_content = [
        {key: value for key, value in item.items() if key not in ['long_memory', 'short_memory']}
        for item in last_content
    ]
    if short_memory_length > len(last_content):
        short_memory = filtered_content
    else:
        short_memory = filtered_content[-short_memory_length:]
    return short_memory





def long_memory_update(long_memory_update_num, inputch):

    # step1.生成完整的prompt
    filtered_content = [
        {key: value for key, value in item.items() if key not in ['long_memory', 'short_memory']}
        for item in inputch.last_content
    ]
    input = template_deepseek(filtered_content[-long_memory_update_num:], 'Prompt_long_memory_default')
    # step2.调用llm推理并将长期记忆更新增加
    long_memory = llm_deepseek(input)
    inputch.content['long_memory'] =  inputch.content['long_memory'] + long_memory #增加内容
    print("记忆更新-----memory_input:", input)
    print("记忆更新-----inputch[long_memory]:", inputch.content['long_memory'])

