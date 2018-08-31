# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/29 11:49
@File   : three.py
@Author : ZZShi
程序作用：
    模拟登录后保存cookies，并寻找密码尝试再次登录
    技术点：
        1、模拟登录
        2、会话维持
"""
import requests
from bs4 import BeautifulSoup


class Login(object):
    """
    模拟登录
    """
    def __init__(self):
        self.url = 'http://www.heibanke.com/lesson/crawler_ex02/'
        self.post_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'
        self.session = requests.session()

    def get_token(self):
        """
        获取登录的token
        :return:
        """
        r = self.session.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        # '<input type="hidden" name="csrfmiddlewaretoken" value="PxcES9W00u0f9rTng2WPP3BkWZMPAUHE">'
        token = soup.find('input', attrs={'type': 'hidden'})['value']
        return token

    def login(self):
        """
        登录
        :return:
        """
        data = {
            'csrfmiddlewaretoken': self.get_token(),
            'username': 'crazy',
            'password': 'szz839090'
        }
        r = self.session.post(self.post_url, data=data)
        if '注销' in r.text:
            print('登录成功。。。')
        else:
            print('登录失败！！！')


class OrderPassword(Login):
    """
    从30以内的数字中找出正确的密码
    """
    def __init__(self):
        Login.__init__(self)

    def find(self):
        self.login()
        for i in range(30):
            data = {
                'csrfmiddlewaretoken': self.get_token(),
                'username': 'ZZShi',
                'password': i
            }
            r = self.session.post(self.url, data=data)
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find('h3').text
            if '密码错误' in info:
                print('{}\t\tpassword:{}'.format(info, i))
            else:
                print('{}\t\tpassword:{}'.format(info, i))
                break

    def run(self):
        self.find()


if __name__ == '__main__':
    fp = OrderPassword()
    fp.run()
