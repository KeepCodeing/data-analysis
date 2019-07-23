# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName jobs_spider
@Author hwz
@Date 2019/7/22 13:37
@ProjectName py-projects
-------功能-------
爬取拉钩网职位信息并绘图
-------坑-------
1. 不知道请求里带了什么参数因此没能通过接口爬取数据
2. 每次爬取不同岗位的数据的大小不一样，因此也没法正确标注数据位置
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from matplotlib import rc


class jobsSpider():
    def __init__(self, city, kd, file_name):
        self.file_name = file_name
        # 使用无界面调试
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.wb = webdriver.Chrome(executable_path=r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe', chrome_options=chrome_options)
        url = 'https://www.lagou.com/jobs/list_{kd}?px=default&city={city}'.format(kd=kd, city=city)
        self.wb.get(url)
        self.data = {
            'title':[],
            'money':[],
            'exp':[],
            'tags':[],
            'company_name':[],
            'industry':[]
        }

    def dataParse(self, html):
        title = html.xpath('//div[@class="s_position_list "]/ul/li//h3/text()')
        money = html.xpath('//div[@class="s_position_list "]/ul/li//div[@class="li_b_l"]/span[@class="money"]/text()')
        exp = html.xpath('//div[@class="s_position_list "]/ul/li//div[@class="li_b_l"]/text()')
        tags = html.xpath('//div[@class="list_item_bot"]/div/span/text()')
        company_name = html.xpath('//div[@class="company_name"]/a/text()')
        industry = html.xpath('//div[@class="industry"]/text()')
        l = [i.replace(' ', '').replace('\n', '') for i in exp]
        exp = [i for i in l if len(i) > 0]
        l = [i.replace(' ', '').replace('\n', '') for i in industry]
        industry = [i for i in l if len(i) > 0]
        self.data['title'].extend(title)
        self.data['money'].extend(money)
        self.data['exp'].extend(exp)
        self.data['tags'].extend(tags)
        self.data['company_name'].extend(company_name)
        self.data['industry'].extend(industry)
        print(self.data)
        print('*'*10)

    def getData(self):
        time.sleep(2)
        print(self.wb.current_url)
        source = self.wb.page_source
        # with open('t.html', 'w') as f:
        #     f.writelines(source)
        html = etree.HTML(source)
        next_page_class = html.xpath('//span[text()="下一页"]/@class')
        if next_page_class:
            if 'pager_next_disabled' not in next_page_class[0]:
                self.dataParse(html)
                self.wb.find_element_by_xpath('//span[text()="下一页"]').click()
                self.getData()
        else:
            self.dataParse(html)
            self.saveJson(self.data, self.file_name)
            self.wb.close()
            self.wb.quit()
            return

    @staticmethod
    def saveJson(data, file_name):
        '''
        保存json文件
        :param data:要保存的文件
        :return:
        '''
        json_str = json.dumps(data)
        with open('./'+file_name+'.json', 'w') as f:
            json.dump(json_str, f)
        print('保存json文件成功')
        json2csv(file_name)

def readJson(file_name):
    '''
    读取json
    :return:
    '''
    with open('./'+file_name+'.json', 'r') as f:
        j_str = json.load(f)
    data = json.loads(j_str)
    return data


def json2csv(file_name):
    d = readJson(file_name)
    n = {i:d[i] for i in d if i != 'tags'}
    df = pd.DataFrame(n)
    df.to_csv('./'+file_name+'.csv')


def start():
    city = input('请输入城市：')
    job = input('请输入职位：')
    file_name = input('请输入json文件名：')
    j = jobsSpider(city=city, kd=job, file_name=file_name)
    j.getData()
    draw(file_name, job)


def draw(file_name, job_name):
    font = {
        'family': 'MicroSoft YaHei',
        'weight': 'normal',
        'size': 13
    }
    rc('font', **font)
    df = pd.read_csv('./'+file_name+'.csv')
    print(df)
    company = df['company_name'].value_counts()[:5]
    arr_len = len(company)
    fig = plt.figure(figsize=(30, 20), dpi=80)
    plt.title(job_name + '岗位')
    # 招收数前五的公司
    index = company.index
    val = company.values
    # n = 0
    # for i in val:
    #     plt.text(i+i*0.1, n, i)
    #     n += 1
    fig.add_subplot(3, 2, 1)
    plt.title('招收数前'+str(arr_len)+'的公司')
    plt.xlabel('数量')
    plt.ylabel('公司名称')
    plt.barh(index, val, label='招收数前'+str(arr_len), color='lime')
    plt.grid()
    plt.legend()
    # 工资集中分布
    money = df['money'].str.split('-')
    min_m = []
    max_m = []
    for i in money:
        min_m.append(i[0])
        max_m.append(i[1])

    min_m = [int(i.lower().replace('k', '')) * 1000 for i in min_m]
    max_m = [int(i.lower().replace('k', '')) * 1000 for i in max_m]
    # n = 0
    # for i in min_m:
    #     plt.text(n, i+i*0.1, str((i/10000))+'w')
    #     n += 1
    # n = 0
    # for i in max_m:
    #     plt.text(n-1, i+i*0.2, str((i/10000))+'w')
    #     n += 1
    fig.add_subplot(3, 2, 2)
    plt.title('最高工资与最低工资分布')
    plt.bar(range(1, len(min_m) + 1), min_m, color='orange', label='最低工资')
    plt.bar(range(1, len(min_m) + 1), max_m, color='cyan', alpha=0.5, label='最高工资')
    plt.grid()
    plt.legend()
    # 招收职位数量

    job = df['title'].value_counts()[:10]
    arr_len = len(job)
    index = job.index
    val = job.values
    # n = 0
    # for i in val:
    #     plt.text(i+i*0.1, n, i)
    #     n += 1
    fig.add_subplot(3, 2, 3)
    plt.title('前' + str(arr_len) + '职位数量')
    plt.barh(index, val, label='职位数', color='darkslategray')
    plt.grid()
    plt.legend()
    # 学历要求
    exp = df['exp'].str.split('/')
    work_time = []
    xl = []
    for i in exp:
        work_time.append(i[0])
        xl.append(i[1])
    xl_df = pd.Series(xl).value_counts()
    index = xl_df.index
    val = xl_df.values
    # n = 0
    # for i in val:
    #     plt.text(n, i+i*0.1, i)
    #     n += 1
    fig.add_subplot(3, 2, 4)
    plt.title('学历要求')
    plt.bar(index, val, label='学历要求', color='orangered')
    plt.grid()
    plt.legend()
    # 经验要求
    exp = df['exp'].str.split('/')
    exp = [i[0] for i in exp]
    exp_df = pd.Series(exp).value_counts()
    index = exp_df.index
    val = exp_df.values
    # n = 0
    # for i in val:
    #     plt.text(i + i*0.1, n, i)
    #     n += 1
    fig.add_subplot(3, 1, 3)
    plt.title('经验要求')
    plt.barh(index, val, color='gold', label='经验要求')
    plt.grid()
    plt.legend()
    plt.show()


def start_draw():
    file_name = input('输入csv文件名：')
    title = input('输入画布标题（分析的行业）：')
    draw(file_name, title)


def main():
    start()


if __name__ == '__main__':
    main()