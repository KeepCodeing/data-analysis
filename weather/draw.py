# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName draw
@Author hwz
@Date 2019/7/19 21:56
@ProjectName py-projects
-------功能-------
绘制天气统计图表
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import  rc
from collections import Counter


def getCount(data):
    return Counter(data)


def highest_t(data):
    plt.subplot(3, 2, 1)
    highest = data
    d = 5
    hist_len = (highest.max() - highest.min()) // d
    plt.title('武汉2018年最高气温分布分析')
    plt.xticks(range(highest.min(), highest.max() + d, d))
    plt.hist(highest, hist_len, label='最高气温', color='crimson')
    plt.legend()
    plt.grid()
    plt.xlabel('最高气温分布')
    plt.ylabel('天数')


def lowest_t(data):
    plt.subplot(3, 2, 2)
    lowest = data
    d = 6
    hist_len = (lowest.max() - lowest.min()) // d
    plt.xticks(range(lowest.min(), lowest.max() + d, d))
    plt.title('武汉2018年最低气温分布分析')
    plt.hist(lowest, hist_len, label='最低气温', color='aquamarine')
    plt.legend()
    plt.grid()
    plt.xlabel('最低气温分布')
    plt.ylabel('天数')


def weather(data):
    plt.subplot(3, 2, 3)
    count = Counter(data)
    weather_name = [i for i in list(dict(count).keys())]
    weather_count = [i for i in list(dict(count).values())]
    plt.title('武汉2018年天气情况分析')
    plt.barh(weather_name, weather_count, label='天气情况', color='cornflowerblue')
    plt.legend()
    plt.grid()
    plt.xlabel('天数')
    plt.ylabel('天气')


def wind_point(data):
    plt.subplot(3, 2, 4)
    count = Counter(data)
    weather_name = [i for i in list(dict(count).keys())]
    weather_count = [i for i in list(dict(count).values())]
    plt.barh(weather_name, weather_count, label='风向', color='turquoise')
    plt.title('武汉2018年风向情况分析')
    plt.legend()
    plt.grid()
    plt.xlabel('天数')
    plt.ylabel('风向')


def wind_power(data):
    # 占满最后两个位置
    plt.subplot(3, 1, 3)
    count = Counter(data)
    weather_name = [i for i in list(dict(count).keys())]
    weather_count = [i for i in list(dict(count).values())]
    plt.barh(weather_name, weather_count, label='风力', color='darkorange')
    plt.title('武汉2018年风力情况分析')
    plt.legend()
    plt.grid()
    plt.xlabel('天数')
    plt.ylabel('风力')


def start():
    data = pd.read_csv('./weather.csv')
    weather_dict = {}
    plt.figure(figsize=(20, 15), dpi=80)
    font = {
        'family': 'MicroSoft YaHei',
        'weight': 'normal',
        'size': 16
    }
    rc('font', **font)
    highest_t(data['最高气温'])
    lowest_t(data['最低气温'])
    weather(data['天气'])
    wind_point(data['风向'])
    wind_power(data['风力'])
    plt.show()
    plt.savefig('./weather.png')


def main():
    start()


if __name__ == '__main__':
    main()