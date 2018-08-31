# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/29 15:01
@File   : five.py
@Author : ZZShi
程序作用：
    尝试密码并进行破解
    技术点：
        1、模拟登陆
        2、会话维持
        3、验证码破解（OCR）
    改进点：
        1、训练字库提高验证码识别的准确率
        2、使用多进程提高速度
"""
import os
import time
from bs4 import BeautifulSoup
from lxml import etree
import tesserocr
from PIL import Image

from three import Login


class Captcha(Login):
    def __init__(self):
        Login.__init__(self)
        self.url = 'http://www.heibanke.com/lesson/crawler_ex04/'
        self.captcha_url = 'http://www.heibanke.com/captcha/image/'
        self.captcha_code = ''
        self.count = 1

    def _token_captcha_code(self):
        """
        获取模拟登录所需提交的信息
        :return:
        """
        try:
            r = self.session.get(self.url)
            tree = etree.HTML(r.text)
            token = tree.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
            captcha_0 = tree.xpath('//input[@id="id_captcha_0"]/@value')[0]
            url = self.captcha_url + captcha_0
            res = self.session.get(url)
            path = 'D:\life\heibanke\challenge\captcha'
            if not os.path.exists(path):
                os.mkdir(path)
            filename = path + '\\' + str(self.count) + '.jpg'
            self.count += 1
            with open(filename, mode='wb') as f:
                f.write(res.content)
            captcha_1 = self.crack_captcha(filename)
            return token, captcha_0, captcha_1
        except Exception as e:
            print('提取验证码失败：', e.args)

    @staticmethod
    def crack_captcha(img):
        """
        验证码识别，对于一些比较斜的字符，识别的正确率不高
        :param img:
        :return:
        """
        try:
            image = Image.open(img)
            # 将图像转换为灰度值
            image = image.convert('L')
            threshold = 120
            table = []
            for i in range(256):
                if i < threshold:
                    table.append(0)
                else:
                    table.append(1)
            # 将图像进行二值化处理
            image = image.point(table, '1')
            result = tesserocr.image_to_text(image).strip()
            print('\t验证码：', result)
            return result
        except Exception as e:
            print('解析验证码失败：', e.args)

    def find_password(self):
        """
        密码破解
        :return:
        """
        password = 0
        code_error_count = 1
        while True:
            print('Testing password：', password)
            token, captcha_0, captcha_1 = self._token_captcha_code()
            data = {
                'csrfmiddlewaretoken': token,
                'username': 'crazy',
                'password': password,
                'captcha_0': captcha_0,
                'captcha_1': captcha_1
            }
            r = self.session.post(self.url, data=data)
            soup = BeautifulSoup(r.text, 'lxml')
            title = soup.find('h3').text
            if '验证码输入错误' in r.text:
                print('\t验证码错误，第%s次\t' % code_error_count)
                print('\t', title)
                code_error_count += 1
                # 此处应该重新测试该密码
                # password += 1
            elif '密码错误' in r.text:
                print('\t密码错误:\t', password)
                print('\t', title)
                password += 1
            else:
                print('*' * 40)
                print('\t恭喜你，你已经找到正确的密码！！！')
                print('\tPassword:', password)
                print('\t', title)
                break

    def run(self):
        self.login()
        self.find_password()


if __name__ == '__main__':
    start = time.time()
    c = Captcha()
    c.run()
    end = time.time()
    print('Time:', end - start)




