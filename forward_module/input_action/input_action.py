###
# 本文件中包含了理解思考的所有方法
###
import re

from EmoAIra.src.prompt import template
from EmoAIra.src.llm import llm_api

# 默认方法
def Input_action_default(config, inputch):
    #step1.生成完整的prompt
    input = template.template_qwen_vl(inputch, 'Prompt_input_action_vl')
    #step2.调用llm推理并计入inputch中
    inputch.content['input_action'] = llm_api.llm_qwen_vl(input,inputch.content['see'])
    #print('推理思考-----input:',input)
    print('推理全程-----inputch[input_action]:',inputch.content['input_action'])

    #step3.解析器提取相应信息
    say_match = re.search(r'说话：(.*?)\n|说话:(.*?)\n', inputch.content['input_action'], re.DOTALL)
    feel_match = re.search(r'感受：(.*?)\n|感受:(.*?)\n', inputch.content['input_action'], re.DOTALL)
    emotion_match = re.search(r'表情：(.*?)\n|表情:(.*?)\n', inputch.content['input_action'], re.DOTALL)
    action_match = re.search(r'动作：(.*?)\n|动作:(.*?)\n', inputch.content['input_action'], re.DOTALL)

    # 提取匹配到的信息，如果搜索不到则设置为空字符串
    inputch.content['say'] = say_match.group(1).strip() if say_match else ''
    inputch.content['feel'] = feel_match.group(1).strip() if feel_match else ''
    inputch.content['emotion'] = emotion_match.group(1).strip() if emotion_match else ''
    inputch.content['action'] = action_match.group(1).strip() if action_match else ''
    #print('推理全程-----input:',input)
    print('推理全程-----inputch[say]:',inputch.content['say'])
    print('推理全程-----inputch[feel]:',inputch.content['feel'])
    print('推理全程-----inputch[emotion]:',inputch.content['emotion'])
    print('推理全程-----inputch[action]:',inputch.content['action'])

