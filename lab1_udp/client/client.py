#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/19'
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
import socket
import json
from PyQt5.QtWidgets import QDialog


class client():
    def __init__(self, socket_connect=None):
        self.socket_connect = socket.socket(socket.AF_INET,
                                            socket.SOCK_DGRAM) if socket_connect == None else socket_connect
        
        self.server_addr = ("127.0.0.1", 23333)
        
        self.token = "0"
        self.id = -1
        # self.socket_connect.connect(self.server_addr)
    
    def login(self, username, password):
        data = {
            "method": "login",
            "parm": {
                "username": username,
                "password": password
            }
        }
        
        data = json.dumps(data).encode("utf-8")
        self.socket_connect.sendto(data, self.server_addr)
        r = self.socket_connect.recv(1024).decode("utf-8")
        response = json.loads(r)
        status = response['status']
        if status == "success":
            self.token = response["token"]
            self.id = self
            return True
        else:
            return False
    
    def register(self, username, password):
        data = {
            "method": "register",
            "parm": {
                "username": username,
                "password": password
            }
        }
        
        data = json.dumps(data).encode("utf-8")
        self.socket_connect.sendto(data, self.server_addr)
        r = self.socket_connect.recv(1024).decode("utf-8")
        response = json.loads(r)
        status = response['status']
        if status == "success":
            self.token = response["token"]
            return True
        else:
            return False
    
    def send_message(self, message, token, to_user):
        data = {
            "method": "send",
            "parm": {
                "token": self.token,
                "message": message,
                "to_user": to_user
            }
        }
        
        data = json.dumps(data).encode("utf-8")
        self.socket_connect.sendto(data, self.server_addr)
        return True
        
    def recv_message(self):
        response = self.socket_connect.recv(1024).decode("utf-8")
        response = json.loads(response)
        if "message" in response or "status" in response:
            return response
        else:
            return False
    
    def log_out(self):
        data = {
            "method": "logout",
            "parm": {
                "token": self.token
            }
        }
        data = json.dumps(data).encode("utf-8")
        self.socket_connect.sendto(data, self.server_addr)


if __name__ == '__main__':
    c = client()
    c.login("hammer", "hammernb")
    print(c.token)
    c.log_out()
