###
# 本文件中包含了理解思考的所有方法
###

from src.prompt import template
from src.llm import llm_api

# 默认方法
def Input_think_default(config, inputch):
    # #step1.生成完整的prompt
    # input = template.template_deepseek(inputch, 'Prompt_input_think_default')
    # #step2.调用llm推理并计入inputch中
    # inputch.content['input_think'] = llm_api.llm_deepseek(input)
    # print('推理思考-----input:',input)
    # print('推理思考-----inputch[input_think]:',inputch.content['input_think'])

    #step1.生成完整的prompt
    input = template.template_qwen_vl(inputch, 'Prompt_input_think_vl')
    #step2.调用llm推理并计入inputch中
    inputch.content['input_think'] = llm_api.llm_qwen_vl(input,inputch.content['see'])
    #print('推理思考-----input:',input)
    print('推理思考-----inputch[input_think]:',inputch.content['input_think'])

