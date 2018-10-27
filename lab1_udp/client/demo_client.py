#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/17'
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
from multiprocessing import Process
import socket
import json

test_data = {
    "login_data1" : {
        "method":"login",
        "parm":{
            "username":"ngc7293",
            "password":"123456",
        }
    },
    "send_data" : {
        "method":"send",
        "parm":{
            "token":"219164e06e1ff3b3994aa529dd429b3b",
            "message":"asfnsajfjasbfjabh",
            "to_id":1
        }
    },
    "reg_data" : {
        "method":"register",
        "parm":{
            "username":"123456",
            "password":"123456",
        }
    },
    "login_data2" : {
        "method":"login",
        "parm":{
            "username":"hammer",
            "password":"hammernb",
        }
    },
}


def login_A():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("127.0.0.1",23333))
    
    login_data = {
        "method":"login",
        "parm":{
            "username":"ngc7293",
            "password":"123456",
        }
    }
    
    sent_data = json.dumps(login_data).encode("utf-8")
    
    s.send(sent_data)
    
    r = s.recv(1024)
    
    print(r)
    
    while True:
        s_string = input("send message:")

        if s_string == "0":
            break
        send_data = {
            "method": "send",
            "parm": {
                "token": "16fb274cec25ee25b9bcbf6b201d71c2",
                "message": s_string,
                "to_id": 3
            }
        }
        
        send_data = json.dumps(send_data).encode("utf-8")
        
        s.send(send_data)
    
    s.close()
    

def login_B():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("127.0.0.1", 23333))
    
    login_data = {
        "method": "login",
        "parm": {
            "username": "hammer",
            "password": "hammernb",
        }
    }
    
    sent_data = json.dumps(login_data).encode("utf-8")
    
    s.send(sent_data)
    
    r = s.recv(1024)
    
    print(r)
    
    while True:
        r = s.recv(1024)
        
        print(r)
        
        s_string = input("send 2message:")
        
        if s_string == "0":
            break
        
    s.close()
    
    
login_A()