from EmoAIra.src.prompt import template
from EmoAIra.src.llm import llm_api


def short_memory_update(config, last_content):
    short_memory_length = config['short_memory_length']
    if short_memory_length > len(last_content):
        short_memory = last_content
    else:
        short_memory = last_content[-short_memory_length:]
    return short_memory





def long_memory_update(config, inputch):

    # step1.生成完整的prompt
    input = template.template_deepseek(inputch, 'Prompt_long_memory_default')

    # step2.调用llm推理并将长期记忆更新增加
    long_memory = llm_api.llm_deepseek(input)
    inputch.content['long_memory'] =  inputch.content['long_memory'] + long_memory #增加内容
    print("记忆更新-----memory_input:", input)
    print("记忆更新-----inputch[long_memory]:", inputch.content['long_memory'])

