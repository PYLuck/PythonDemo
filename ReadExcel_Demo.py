# 读取 xls（Excel 97-2003）和xlsx（Excel 2007及以上）分类数据集

import xlrd
import pandas as pd

import os
import torch
import numpy as np
from pathlib import Path
from torch.utils.data import Dataset
import random
from tqdm import tqdm



# 数据集预处理--先逐行读出所有数据
class DataSetHandle(Dataset):
    def __init__(self, data_all_list, proportion, list_tuple=None):
        """
        :type data_all_list: list
        """
        self.data_all_list = data_all_list
        # 按文件夹读取分类标签
        self.sub_files_list = [info.name for info in Path(self.data_all_list[0]).iterdir() if Path.is_dir(info)]    # ['SY', 'WHZ']
        self.label_map = dict((info, index) for index, info in enumerate(self.sub_files_list))  # {'SY': 0, 'WHZ': 1}
        self.proportion = proportion        # 划分比例

        self.list_tuple = list_tuple
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 搬运至GPU必要的 类方法
    def __getitem__(self, item):
        return torch.FloatTensor(self.list_tuple[item][0]).to(self.device),\
                    torch.tensor(self.list_tuple[item][1]).to(self.device)

    def __len__(self):
        return len(self.list_tuple)


    def file2Tensor(self):
        train_set, dev_set, test_set = self.file2List()
        # 实现List转Tensor, 传递list_tuple参数(其他不变)
        train_set = DataSetHandle(self.data_all_list,self.proportion, list_tuple=train_set)
        dev_set = DataSetHandle(self.data_all_list,self.proportion, list_tuple=dev_set)
        test_set = DataSetHandle(self.data_all_list,self.proportion, list_tuple=test_set)

        return train_set, dev_set, test_set

    # 划分数据集
    def file2List(self):
        Xls_list = self._Xls2list(self.data_all_list)
        random.shuffle(Xls_list)

        train_num = int(len(Xls_list) * self.proportion[0] / 10)
        dev_num = int(len(Xls_list) * self.proportion[1] / 10)
        # 划分比例
        train_list = Xls_list[0:train_num]
        dev_list = Xls_list[train_num: train_num + dev_num]
        test_list = Xls_list[train_num + dev_num:]

        return train_list, dev_list, test_list

    # 数据预处理, 打标签
    def _Xls2list(self, data_all_list):
        global nrows, AB_Breath, AB_Heart
        all_list = []
        for data_all in data_all_list:
            for sub_files in self.sub_files_list:
                # os.walk()返回生成器
                one_Pre_files = next(os.walk(top=data_all + '/' + sub_files))[2]      # next()后得到(root,dirs,files),取files列表


                for Pre in tqdm(one_Pre_files):
                    df = pd.read_excel(data_all + '/' + sub_files + '/' + Pre)
                    a_data = df.loc[[i for i in range(0, 30)]].values        # ndaarry:读取指定多行的话，就要在loc[]里面嵌套列表指定行数
                    a_data = np.delete(a_data, obj=0, axis=1)           # 去除第一列
                    nrows = a_data.shape[0]  # 行数

                    # 预处理：单个数据分割
                    try:
                        if Pre.startswith('Breath'):
                            AB_Breath = []
                            for ri in range(nrows):
                                AB_Breath.append(a_data[ri, 0:50])
                                AB_Breath.append(a_data[ri, 50:])

                        elif Pre.startswith('Heart'):
                            AB_Heart = []
                            for ri in range(nrows):
                                AB_Heart.append(a_data[ri, 0:50])
                                AB_Heart.append(a_data[ri, 50:])

                    except ValueError:
                        print(data_all + '/' + sub_files + '/' + Pre)

                # 将每个人的呼吸和心率组合
                for row in range(2*nrows):
                    a_BH = np.c_[AB_Breath[row], AB_Heart[row]]

                    # 打标签
                    label = self.label_map[sub_files]  # 取字典的Value作为标签
                    all_list.append((a_BH, label))




        # return 所有处理后的 数据+标签: [(样本1,标签1),...]
        print('组合样本总数:{0}'.format(len(all_list)))
        return all_list











if __name__ == '__main__':
    data_all_list = ['DataLoad/BreathHeart']
    train_set, dev_set, test_set = DataSetHandle(data_all_list, [6, 2, 2]).file2Tensor()

