###
# 该代码实现了 针对不同场景进行不同prompt-template的拼接
###

from EmoAIra.src.prompt import all_prompt

# 适配deepseek的封装方法
def template_deepseek(inputch, prompt_category):

    #基于不同的入参选择不同的prompt封装成template
    #1
    if prompt_category == 'Prompt_input_think_default':
        prompt = all_prompt.Prompt_input_think_default
        contents = f'''
记忆：{inputch.content['long_memory']}。{inputch.content['short_memory']}
对话：{inputch.content['talk']}
心情：{inputch.content['mood']} 
'''
    #2
    elif prompt_category == 'Prompt_think_action_default':
        prompt = all_prompt.Prompt_think_action_default
        contents = f'''
{inputch.content['input_think']}
心情：{inputch.content['mood']}
'''

    #3
    elif prompt_category == 'Prompt_long_memory_default':
        prompt = all_prompt.Prompt_long_memory_default
        contents = f'''
短期记忆：{inputch.content['long_history']}
'''

    #0
    else:
        prompt = all_prompt.Prompt_input_think_default
        contents = f'''
记忆：{inputch.content['long_history']}。{inputch.content['short_history']}
对话：{inputch.content['talk']}
心情：{inputch.content['mood']} 
'''

    #将信息写进适配的格式中
    result = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": contents},
    ]
    return result



