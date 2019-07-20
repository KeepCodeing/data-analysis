# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName dog_test
@Author hwz
@Date 2019/7/18 21:08
@ProjectName py-projects
-------功能-------
简单分析狗名数据
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rc


def name_use_count(dg):

    font = {
        'family':'MicroSoft YaHei',
        'weight':'bold',
        'size':10
    }
    rc('font', **font)
    name_count = dg.loc[:, 'Count_AnimalName'].values
    # print(list(name))
    name_max = name_count.max()
    name_min = name_count.min()
    # 组距
    hist_len = 100
    # 组数
    group_len = (name_max - name_min) // hist_len
    print(name_max, name_min, hist_len)
    plt.hist(name_count, group_len, label='数量')
    plt.grid()
    plt.xticks(range(name_min, name_max+hist_len, hist_len))
    plt.yticks()
    plt.xlabel('数量')
    plt.ylabel('使用数')
    plt.title('狗名数量分布')

    plt.show()

    # print(dg.loc[:, 'Count_AnimalName'])

    # 前五条数据
    # print(dg.head())
    # 文件信息
    # print(dg.info())
    # print(dg.sort_values(by='Count_AnimalName', ascending=False).head(5))


def top_n_counter(dg, l=0, n=0):
    font = {
        'family':'MicroSoft YaHei',
        'weight':'normal',
        'size':16
    }
    rc('font', **font)
    # 统计前n个使用的名字的使用数
    sorted_name = dg.sort_values(by='Count_AnimalName', ascending=False)
    top_five = sorted_name[l:n].values
    name_list = []
    count_list = []
    for i in top_five:
        name_list.append(i[0])
        count_list.append(i[1])
    plt.figure(figsize=(20, 8), dpi=80)
    plt.title('狗名使用次数统计')
    plt.xlabel('使用次数')
    plt.ylabel('狗名')
    plt.barh(name_list, count_list, label='狗名', height=0.5, color='r')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    dg = pd.read_csv('./dogNames2.csv')
    # top_n_counter(dg, l=5, n=10)
    data = dg.sort_values(by='Count_AnimalName', ascending=False)
    print(type(data['Count_AnimalName'].unique()))