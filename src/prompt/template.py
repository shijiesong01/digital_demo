from EmoAIra.src.prompt import all_prompt

def template_deepseek(inputch, prompt_category):

    #基于不同的入参选择不同的prompt封装成template
    #1
    if prompt_category == 'Prompt_input_think_default':
        prompt = all_prompt.Prompt_input_think_default
        contents = f'''
记忆：{inputch.content['long_history']}。{inputch.content['short_history']}
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



def template_long_memory(inputch, prompt_category):
    # 基于不同的入参选择不同的prompt封装成template
    # 1
    if prompt_category == 'prompt_long_memory_default':
        prompt = all_prompt.Prompt_long_memory_default
        contents = f'''
短期记忆：{inputch.content['long_history']}
    '''

    # 3
    else:
        prompt = all_prompt.Prompt_long_memory_default
        contents = f'''
短期记忆：{inputch.content['long_history']}
总结：'''

    # 将信息写进适配的格式中
    result = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": contents},
    ]
    return result
