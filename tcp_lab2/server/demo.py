#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
import threading

class a(object):
    def __init__(self):
        self.abc = 2
        
    def a(self):
        t1 = threading.Thread(target=self.c)
        t = threading.Thread(target=self.b)
        t1.start()
        t.start()
        
    def c(self):
        self.abc = 3
        
    def b(self):
        print(self.abc)
        
if __name__ == '__main__':
    a().a()