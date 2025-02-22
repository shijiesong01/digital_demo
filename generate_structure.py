###
# 用于生成项目代码结构，直接运行该项目即可
###

import os

def generate_project_structure(path, prefix=''):
    items = os.listdir(path)
    for index, item in enumerate(items):
        full_path = os.path.join(path, item)
        is_last = index == len(items) - 1
        if os.path.isdir(full_path):
            print(prefix + ('└── ' if is_last else '├── ') + item + '/')
            new_prefix = prefix + ('    ' if is_last else '│   ')
            generate_project_structure(full_path, new_prefix)
        else:
            print(prefix + ('└── ' if is_last else '├── ') + item)

# 替换为项目的根目录
project_root = '.'
generate_project_structure(project_root)

'''
python generate_structure.py > project_structure.txt
'''
