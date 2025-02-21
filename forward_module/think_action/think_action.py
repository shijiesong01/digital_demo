###
# 本文件中包含了决策动作的所有方法
###
from EmoAIra.src.prompt import template
from EmoAIra.src.llm import llm_api
import re
# 默认方法
def Think_action_default(config, inputch):
    #step1.生成完整的prompt
    input = template.template_deepseek(inputch, 'Prompt_think_action_default')

    #step2.调用llm推理
    think_action = llm_api.llm_deepseek(input)
    #print("think_action:",think_action)

    #step3.解析器提取相应信息
    say_match = re.search(r'回答：(.*?)\n|回答:(.*?)\n', think_action, re.DOTALL)
    feel_match = re.search(r'感受：(.*?)\n|感受:(.*?)\n', think_action, re.DOTALL)
    emotion_match = re.search(r'表情：(.*?)\n|表情:(.*?)\n', think_action, re.DOTALL)
    action_match = re.search(r'动作：(.*?)\n|动作:(.*?)\n', think_action, re.DOTALL)

    # 提取匹配到的信息，如果搜索不到则设置为空字符串
    inputch.content['say'] = say_match.group(1).strip() if say_match else ''
    inputch.content['feel'] = feel_match.group(1).strip() if feel_match else ''
    inputch.content['emotion'] = emotion_match.group(1).strip() if emotion_match else ''
    inputch.content['action'] = action_match.group(1).strip() if action_match else ''
    print('推理行动-----input:',input)
    print('推理行动-----inputch[say]:',inputch.content['say'])
    print('推理行动-----inputch[feel]:',inputch.content['feel'])
    print('推理行动-----inputch[emotion]:',inputch.content['emotion'])
    print('推理行动-----inputch[action]:',inputch.content['action'])

