# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName get2018weather
@Author hwz
@Date 2019/7/19 16:38
@ProjectName py-projects
-------功能-------
获取武汉2018年的历史天气
-------遇到的坑------
1. 获取页面时请求头里没有带上cookie，导致获取的页面是404页面
2. 观察页面源码时使用了Chrome的检查功能，然而里面的元素排列并不是真正的页面元素顺序
3. IDE编码设置成了GBK，导致UTF-8编码的中文乱码
4. 使用了多线程但是是一次性将数据返回，但在写入时又遍历了遍数据导致文件写入出现问题
"""
import requests
import json
import pandas as pd
from lxml import etree
from ua import getUa
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


class crawlWeather():
    def __init__(self, city, year):
        self.url = 'http://lishi.tianqi.com/{city}/index.html'.format(city=str(city))
        self.xpath_str = '//div[@class="tqtongji1"]//ul/li/a[contains(text(), "{year}")]/@href'.format(year=str(year))
        self.s = requests.Session()
        self.s.headers = {
            'Cookie': 'cityPy={city}; cityPy_expire=1564130059'.format(city=city),
            'User-agent': getUa(),
        }

    def getWeatherQueue(self):
        '''
        获取历史天气列表并以队列形式返回
        :return:
        '''
        html = self.s.get(url=self.url)
        if self.url != html.url:
            print('获取页面失败！请检查Cookie！')
            return None
        parse_html = etree.HTML(html.text)
        weather_queue = Queue()
        url_list = parse_html.xpath(self.xpath_str)
        url_list.reverse()
        self.list_len = len(url_list)
        for i in url_list:
            weather_queue.put(i)
        weather_queue.put(None)
        return weather_queue

    def getWeatherInfo(self, weather_queue):
        '''
        获取天气详情
        :param weather_queue: url队列
        :return:
        '''
        data = []
        while True:
            url = weather_queue.get()
            if url is not None:
                html = self.s.get(url=url)
                parse_html = etree.HTML(html.text)
                ul = parse_html.xpath('//div[@class="tqtongji2"]/ul')
                for u in ul[1:]:
                    data.append(u.xpath('li/text()'))
            else:
                print('获取完毕！')
                return data

    def startCrawl(self, j=True, c=False):
        '''
        对功能的整合，使用了线程池
        :param j: 是否保存json文件的参数
        :param c: json转换csv
        :return:
        '''
        weather_queue = self.getWeatherQueue()
        pool = ThreadPoolExecutor(max_workers=3)
        ret = pool.submit(self.getWeatherInfo, weather_queue)
        data = ret.result()
        if j:
            self.keepJson(data)

        if c:
            self.json2Csv()
        pool.shutdown()


    @staticmethod
    def keepJson(data):
        '''
        保存json文件
        :param data:要保存的文件
        :return:
        '''
        json_str = json.dumps(data)
        with open('./weather.json', 'w', encoding='gbk') as f:
            json.dump(json_str, f)
        print('保存json文件成功')


    @staticmethod
    def json2Csv():
        data = readJson()
        month = [i for i in data]
        columns = ['最高气温', '最低气温', '天气', '风向', '风力']
        d = pd.DataFrame(month, index=range(1, len(month) + 1), columns=columns)
        # 保存csv文件
        d.to_csv('./weather.csv')


def readJson():
    '''
    读取json
    :return:
    '''
    with open('./weather.json', 'r') as f:
        j_str = json.load(f)
    data = json.loads(j_str)
    return data


def main():
    w = crawlWeather('wuhan', '2018')
    w.startCrawl(True, True)
    # print(readJson())


if __name__ == '__main__':
    main()