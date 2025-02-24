

def update_Character(config, feel):
    '''
    更新得到最新对话输入时的心情
    :param config: 包含输入时固定性格
    :param feel: 上一轮的感受
    :return: 本轮结合性格和感受的心情
    '''
    character = config["character"]
    if feel != '':
        mood = character + '， 感受：' + feel
    else:
        mood = character

    return mood
