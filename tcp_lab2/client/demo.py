#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/13'
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
import sys,time
for i in range(101):
    s1 = "\r%d%%[%s%s]\n"%(i,"*"*i," "*(100-i))
    s2 = "\r%d%%[%s%s]"%(i,"*"*i," "*(100-i))
    sys.stdout.write(s1)
    sys.stdout.write(s2)
    sys.stdout.flush()
    time.sleep(0.03)