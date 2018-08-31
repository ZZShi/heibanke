# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/29 0:24
@File   : one.py
@Author : ZZShi
程序作用：
    提取网页中的信息作为下一次请求的链接
    技术点：
        1、网页解析
        2、正则表达式
"""
import re
import requests
from bs4 import BeautifulSoup


def run():
    url = 'http://www.heibanke.com/lesson/crawler_ex00/'
    result = ''
    while True:
        real_url = url + result
        try:
            r = requests.get(real_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            h3 = soup.find('h3').text
            print(h3)
            result = re.search(r'\d{5}', h3, re.S).group(0)
        except:
            print('Ended...')
            break


if __name__ == '__main__':
    run()
