from pathlib import Path

# 读取该项目下的所有以 _demo.py结尾的文件
# 将更新的Demo 写入 ReadMe.md

Part_Star = "# 这是一个demo的存放项目\n #### 主要存放各类功能函数的方法，用于后续的学习与使用。" \
            "\n##### 例如：argpase_demo.py 存放的是import argpase的使用方法" \
            "\n注：**Write2ReadMe.py** 是用于将本项目中的所有.py文件(即功能函数_demo)**更新**到ReadMe.md中\n"
with open('./ReadMe.md', 'w', encoding='utf-8') as f:
    f.writelines(Part_Star + '目录:\n')
    for file in Path(__file__).parent.rglob('*_Demo.py'):
        firstLine = open(str(file), 'r', encoding='utf-8')
        f.write(str(file) + '\n Info: ' + firstLine.readline() + '\n')
        firstLine.close()

print('更新完成！')
