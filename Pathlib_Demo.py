""" pathlib 库从 python3.4 开始，到 python3.6 已经比较成熟 """
"""
老的路径操作函数管理比较混乱，有的是导入 os, 有的又是在 os.path 当中，新用法统一用 pathlib 管理。
老用法处理不同操作系统 win，mac linux 之间很吃力。换了操作系统常常要改代码。
老用法主要是函数形式，返回的数据类型通常是字符串。但是路径和字符串并不等价。
新用法是面向对象，处理起来更灵活方便。 
"""

from pathlib import Path
'''注：Path()获取到的地址类型是<class 'pathlib.WindowsPath'>，需要str()转字符'''

# 路径获取
Path.cwd()          # <class 'pathlib.WindowsPath'>
str(Path.home())                # C:\Users\PyLuck
# 获取当前文件路径;     父级路径:Path(__file__).parent;     绝对路径.absolute()
print(Path(__file__))           # 在pycharm中运行的结果：F:\经济技术开发区\DemoProj\Pathlib_Demo.py   在cmd中运行：Pathlib_Demo.py

# 获取路径组成部分
file = Path('./test.py')
print(file.match('*.py'))       # True 检查文件后缀是否匹配
# 文件名, 后缀, 父级(cd ..), 目录前面的部分
print(file.stem, file.suffix, file.parent, file.anchor)     # test .py

# 子路径扫描
files = Path('DataLoad/dataTest')       # 先获取子路径
# if files.is_dir() 判断是否为 文件夹            # if files.exists   判断是否 存在
print([str(sub.stem) for sub in files.iterdir() if files.is_dir()])     # ['001end', '002end', '003end', '004end']
'''
files = Path('DataLoad/BreathHeart')
# subFile = [sub.stem for sub in files.iterdir() if files.is_dir()]   # 遍历 子文件
for sub in files.iterdir():
    if files.is_dir():
        for Per in sub.iterdir():
            if sub.with_name('*.xlsx'):
                print(str(Per))
'''

# 路径拼接，用 / 拼接
print(str(Path.home() / 'dir' / 'file.txt'))     # C:\Users\PyLuck\dir\file.txt

# 创建文件 + touch判断文件存在
fi = Path('ReadMe.md')          # 创建一个.md文件
print(fi.touch(exist_ok=True))          # 输出 None 表示文件已存在
# 创建目录.mkdir()  .mkdir(parents=True)可以创建多级目录
Path('./Test').mkdir()         # 文件夹已存在时无法创建
Path('./Test').rmdir()        # 删除目录    .unlink用于删除文件

# 打开文件，可传入Path对象
with open(Path('./readMe.md'), encoding='utf-8') as f:
    print(f.read())

# 移动文件 原地址.replace(新地址)
Path("demo.txt").replace('archive/demo.txt')
# 为了避免同名文件被覆盖，一般用法：
dest = Path('new_demo.txt')
if (not dest.exists()) and dest.parent.exists():
    Path("demo.txt").replace(dest)

# 重命名文件
newFile = Path("demo.txt").with_name('new.txt')
Path("demo.txt").replace(newFile)



