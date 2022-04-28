"""对文件进行批量操作：批量重命名"""
# -*- coding: utf-8 -*-
# Ref: https://blog.csdn.net/Yao_June/article/details/92416562
import os, sys


class File_Rename(object):
    def __init__(self, path, backName):
        self.path = path  # 要改的路径
        self.backName = backName  # 要批量改的文件共同后缀(特征)-.txt
        self.fileList = os.listdir(self.path)  # 以list读取path文件夹下-所有文件

    def EndName(self, Back):
        self.Back = Back

        for file in self.fileList:
            if file != sys.argv[0]:  # 防止脚本文件放在path路径下时，被一起重命名
                if file.endswith(self.backName):
                    end = file.replace(self.backName, self.Back)  # 增加后缀
                    os.rename(os.path.join(self.path, file), os.path.join(self.path, end))
        print("后缀添加完成")

    def StartName(self, nameStart):
        self.nameStart = nameStart
        for file in self.fileList:
            if file != sys.argv[0]:                 # 防止脚本文件放在path路径下时，被一起重命名
                if file.endswith(self.backName):
                    os.rename(os.path.join(self.path, file), os.path.join(self.path, self.nameStart + file))
        print("前缀添加完成")

    def Renumber(self, num_i: float, clean=True):
        self.num = num_i + len(self.fileList) - 1           # 从num_i开始加序号
        _mode = '0' + str(self.num) + self.backName         # 后缀格式
        for file in self.fileList:
            if file != sys.argv[0]:         # 防止脚本文件放在path路径下时，被一起重命名
                if file.endswith(self.backName):
                    if clean:
                        try:
                            os.rename(os.path.join(self.path, file), os.path.join(self.path, '00' + str(self.num) + self.backName))
                        except Exception:
                            print("不能重复操作，请修改初始序号")
                    else:
                        end = file.replace(self.backName, _mode)  # 增加后缀
                        os.rename(os.path.join(self.path, file), os.path.join(self.path, end))
            self.num -= 1
        print("添加序号结束")


if __name__ == '__main__':

    path = r".\DataLoad\dataTest"   # 接口1：需要命名的文件夹
    backName = '.txt'               # 接口2：需要确定的后缀名
    nameEnd = 'end'                 # 接口3：修改的内容--增加后缀(如end)，如'end.txt'
    nameStart = 'Star'              # 接口4：修改的内容--增加前缀，如'Starxxxend.txt'
    Back = nameEnd + backName
    # 确定要修改的路径和后缀
    rename = File_Rename(path, backName)
    # 以下是需要进行修改的格式
    rename.Renumber(1)              # 以 00+float类型的数字 作为文件名后缀 （）中填一个起始的数字
    # rename.EndName(Back)          # 以 nameEnd 作为后缀
    # rename.StartName(nameStart)   # 以 nameStart 作为前缀
