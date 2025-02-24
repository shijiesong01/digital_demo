###
# 本文件中包含了动作输出的所有方法
###
from EmoAIra.forward_module.action_output import live2d

# 默认方法
def Action_output_default(config, inputch, unity_connection):
    ###
    # 1. live2d输出
    ###
    if unity_connection != None and inputch.content['emotion']!= None:
        # 如果对上了unity中的动作参数，则触发更新函数，发送动作参数
        if inputch.content['emotion'] == '微笑':
            live2d.live2d_unity_update(unity_connection, 'proud')
            print('动作输出-----unity成功展示：微笑proud')
        elif inputch.content['emotion'] == '发愁':
            live2d.live2d_unity_update(unity_connection, 'thinking')
            print('动作输出-----unity成功展示：发愁thinking')
        else:
            pass

