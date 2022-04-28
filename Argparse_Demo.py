# 标准库，用于命令行参数解析，将参数与代码分离；自动生成帮助文档
"""
argparse 模块可以让人轻松编写用户友好的命令行接口。
程序定义它需要的参数，然后 argparse 将弄清如何从 sys.argv 解析出那些参数。
argparse 模块还会自动生成帮助和使用手册，并在用户给程序传入无效参数时报出错误信息。
"""
import math
import argparse

# 创建解析器, 添加参数
parser = argparse.ArgumentParser(description='圆柱体积计算器')
parser.add_argument('-r', '--rad', type=int, required=True, help='圆柱半径',default=2)  # --选择性参数
parser.add_argument('-H','--height', required=True, type=int, help='圆柱高度')  # required=True表示为必须的参数

# 互斥锁，不能同时执行以下2个指令
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action='store_true', help='仅输出值')
group.add_argument('-v', '--verbose', action='store_true', help='详细描述')

# 解析参数
args = parser.parse_args()



def compute_value(rad, height):
    value = math.pi * (rad ** 2) * height
    return value

if __name__ == '__main__':

    vol = compute_value(args.rad, args.height)          # 这里rad，height == parser.add_argument的--rad保持一致
    if args.quiet:
        print(vol)      # 加入-q
    elif args.verbose:
        print('圆柱的半径为{},高度为{}，体积计算结果为{}'.format(args.rad, args.height, vol))    # 加入-v
    else:
        print('圆柱体积为%s' % vol)          # -q -v 两个都不输入


# 在终端调用
"""
(python3) D:\PycharmProject\Proj001>python argparse_demo.py -H 4 -r 2 -v
圆柱的半径为2,高度为4，体积计算结果为50.26548245743669

(python3) D:\PycharmProject\Proj001>python argparse_demo.py -H 4 -r 2 -q
50.26548245743669

(python3) D:\PycharmProject\Proj001>python argparse_demo.py -H 4 -r 2
圆柱体积为50.26548245743669
"""
