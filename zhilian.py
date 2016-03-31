#!/usr/bin/env python
# coding:utf-8

import requests
# from bs4 import BeautifulSoup


class Zhilian(object):
    __account = '15638367126'
    __passwd = 'fei1234'

    def __init__(self):
        self.sess = requests.session()

    def login(self):
        payload = {
            # input hidden
            'int_count': '999',
            'errUrl': 'https://passport.zhaopin.com/account/login',
            'RememberMe': 'true',
            'requestFrom': 'portal',
            # account passwd
            'loginname': self.__account,
            'Password': self.__passwd,
        }

        r = self.sess.post('https://passport.zhaopin.com/account/login', data=payload)
        r = self.sess.get('http://i.zhaopin.com/')
        r = self.sess.get('http://i.zhaopin.com/Home/ResumePreview?resumeNumber=JM672449643R90250000000&resumeId=241431445&version=1&language=1&fromtype=popdiv')
        # write file
        with open('cv.html', 'w') as f:
            f.write(r.text)

if __name__ == '__main__':
    zhilian = Zhilian()
    zhilian.login()
