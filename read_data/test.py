# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName test
@Author hwz
@Date 2019/7/18 19:41
@ProjectName py-projects
-------功能-------
测试pandas读取外部数据
"""
import pandas


def read_csv(path):
    csv = pandas.read_csv(path)
    return csv


def read_clipboard():
    return pandas.read_clipboard()


def main():
    # read_csv(r'./dogNames2.csv')
    print(read_clipboard())


if __name__ == '__main__':
    main()