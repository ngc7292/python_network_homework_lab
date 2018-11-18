#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
import sys
from socket import *
import json

IP = "0.0.0.0"
PORT = 23333
HOST = (IP, PORT)

EMPTY = 0
BLACK = 1
WHITE = 2

START_TEXT = """



"""

WIN_TEXT = """



"""


def check_location(point):
    x, y = point
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    else:
        return True


class Client(object):
    def __init__(self, signal):
        self.cli_sock = socket(AF_INET, SOCK_STREAM)
        self.cli_sock.connect(HOST)
        self.signal = signal

    def check_signal(self):
        pass

    def do_recv(self):
        pass

    def recv_message(self, data):
        try:
            data = json.loads(data.decode("utf-8"))
            data['req'] = json.loads(data['req'])
            return data
        except Exception as e:
            print(e)
    
    def send_message(self, data):
        """
        send to cli_sock
        :param data: dict
        :return: NULL
        """
        send_data = json.dumps(data)
        self.cli_sock.sendall(send_data.encode("utf-8"))
    
    def send_search_game(self):
        request = {
            'method': 'search',
            'parm': 'null'
        }
        self.send_message(request)
    
    def send_join_game(self, room_id):
        if room_id == "":
            return
        room_id = str(room_id)
        request = {
            'method': 'join',
            'parm': {
                'room_id': room_id
            }
        }
        self.send_message(request)
    
    def send_create_game(self):
        request = {
            'method': 'create',
            'parm': 'null'
        }
        self.send_message(request)
    
    def send_put(self, point_location):
        parm = {
            'point_location': point_location,
            'room_id': self.room_id
        }
        request = {
            'method': 'put',
            'parm': json.dumps(parm)
        }
        self.send_message(request)
    
    def recv_join(self, req):
        self.room_id = req['room_id']
        self.user_color = req['user_color']
    
    def recv_create(self, req):
        self.room_id = req['room_id']
        self.user_color = req['user_color']
    
    def recv_rput(self, req):
        status = req['status']
        point_location = req['point_location']
        user_color = BLACK if self.user_color == WHITE else WHITE
        
        if status == "1":
            return True
        else:
            return False