#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/20'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import socket
from multiprocessing import Process

def recv_data(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            print(data.decode("utf-8"))
        except Exception as e:
            print(e)
            break

if __name__ == '__main__':
    cli_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cli_sock.connect(("127.0.0.1",23333))
    
    p = Process(target=recv_data,args=(cli_sock, ))
    p.start()
    
    while True:
        try:
            a = input()
            cli_sock.sendall(a.encode("utf-8"))
        except:
            break
            
    print("goodbye")
