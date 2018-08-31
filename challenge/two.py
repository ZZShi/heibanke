# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/29 11:28
@File   : two.py
@Author : ZZShi
程序作用：
    寻找密码并模拟登录
    技术点：
        1、网页解析
        2、模拟登录
"""
import requests
from bs4 import BeautifulSoup


def run():
    url = 'http://www.heibanke.com/lesson/crawler_ex01/'
    for i in range(30):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
        data = {
            'csrfmiddlewaretoken': token,
            'username': 'crazy',
            'password': i
        }
        r = requests.post(url, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.find('h3').text
        if info == "您输入的密码错误, 请重新输入":
            print('{}\t\tpassword:{}'.format(info, i))
        else:
            print('{}\t\tpassword:{}'.format(info, i))
            break


if __name__ == '__main__':
    run()

