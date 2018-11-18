#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/13'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
#!/usr/bin/env python3

import time
from multiprocessing import Process,Queue

q = Queue()  #创建列队，不传数字表示列队不限数量
for i in range(11):
    q.put(i)

def A():
    while 1:
        try:
            num = q.get_nowait()
            print('我是进程A,取出数字:%d'%num)

            time.sleep(1)
        except :
            break

def B():
    while 1:
        try:
            num = q.get_nowait()
            print('我是进程B,取出数字:%d'%num)
            time.sleep(1)
        except :
            break

if __name__ == '__main__':

    p1 = Process(target = A)
    p2 = Process(target = B)
    p1.start()
    p2.start()