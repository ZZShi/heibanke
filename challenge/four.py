# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/29 12:54
@File   : four.py
@Author : ZZShi
程序作用：
    模拟登录后维持会话，从多个网页中解析出密码之后进行处理再次模拟登录
    技术点：
        1、模拟登录
        2、会话维持
        3、网页解析
        4、密码破解
        5、多进程
    改进点：
        1、多线程只能同时开两个，开的多了会出现请求异常
"""
import time
from bs4 import BeautifulSoup
from three import Login
import threading


class RandomPassword(Login):
    """
    从网页中提取出有效信息并破解
    """
    def __init__(self):
        Login.__init__(self)
        self.url = 'http://www.heibanke.com/lesson/crawler_ex03/'
        self.post_url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/'
        self.ps_list_url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page='
        self.password_dict = {}
        self.password = ''

    def get_one_page_password(self, page):
        """
        提取该页的有效信息
        :param page:
        :return:
        """
        print('正在获取第{}页密码...'.format(page))
        url = self.ps_list_url + str(page)
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        ps_poss = soup.find_all('td', attrs={'title': 'password_pos'})
        ps_vals = soup.find_all('td', attrs={'title': 'password_val'})
        if len(ps_poss) == len(ps_vals):
            for ps_poss, ps_vals in zip(ps_poss, ps_vals):
                pos = ps_poss.text
                val = ps_vals.text
                gLock.acquire()
                self.password_dict[int(pos)] = val
                gLock.release()
            print('{}\t\t{}'.format(page, self.password_dict))

    def get_password(self):
        """
        使用多线程提取信息
        :return:
        """
        th = []
        while len(self.password_dict) != 100:
            pages = [page for page in range(1, 14)]
            while len(pages):
                # 为什么只能开两个线程
                for i in range(2):
                    if len(pages):
                        page = pages.pop()
                        t = threading.Thread(target=self.get_one_page_password, args=(page, ))
                        t.start()
                        th.append(t)
                    else:
                        print('页数已经循环完毕...')
                        break
                for t in th:
                    t.join()
        self.password_process()

    def password_process(self):
        """
        密码破解
        :return:
        """
        keys = sorted(self.password_dict.keys())
        print(keys)
        for key in keys:
            value = self.password_dict[key]
            self.password += value
        print(self.password)
        return self.password

    def finally_login(self):
        """
        模拟登录
        :return:
        """
        data = {
            'csrfmiddlewaretoken': self.get_token(),
            'username': 'crazy---',
            'password': self.password
        }
        try:
            res = self.session.post(self.url, data=data)
            soup = BeautifulSoup(res.text, 'lxml')
            title = soup.find('h3').text
            if '成功' in res.text:
                print('登录成功：', title)
            else:
                print('登录失败：', title)
        except Exception as e:
            print('登录发生异常', e.args)

    def run(self):
        self.login()
        self.get_password()
        self.finally_login()


if __name__ == '__main__':
    start = time.time()
    gLock = threading.Lock()
    r = RandomPassword()
    r.run()
    end = time.time()
    print('*' * 40)
    print('Time:', end - start)
