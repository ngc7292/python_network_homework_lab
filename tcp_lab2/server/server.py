#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'
"""
import json
import random
from socket import *
from logging import *
from gomoku import *
import threading

HOST = "0.0.0.0"
PORT = 23333
AC_CLIENT = 1024


class Server(object):
    def __init__(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind((HOST, PORT))
        self.server_sock.listen(AC_CLIENT)
        
        info("have listening in"+str((HOST,PORT)))
        self.Groom_list = {}
        self.Groom_num = 0
        
        self.do_accept()
    
    def do_accept(self):
        while True:
            try:
                cli_sock, cli_host = self.server_sock.accept()
                
                t = threading.Thread(target=self.do_recv,args=(cli_sock,cli_host,))
                
                t.start()
            except BaseException as e:
                error(e)
    
    def do_recv(self, cli_sock, cli_host):
        while True:
            recv_data = cli_sock.recv(1024)
            
            try:
                json_data = json.loads(recv_data.decode("utf-8"))
                method = json_data['method']
                if method == 'search':
                    self.search_room(cli_sock)
                elif method == 'create':
                    self.create_room(cli_sock, cli_host)
                elif method == 'join':
                    self.join_room(cli_sock, cli_host, json_data['parm'])
                elif method == 'put':
                    self.put_point(cli_sock, cli_host, json_data['parm'])
                else:
                    break
            except Exception as e:
                error("data load error")
                error(e)
        cli_sock.shutdown(2)
    
    def search_room(self, cli_sock):
        room_id_list = json.dumps(list(self.Groom_list.keys()))
        response = {
            'method': 'search',
            'req': room_id_list
        }
        response = json.dumps(response)
        cli_sock.sendall(response.encode("utf-8"))
    
    def create_room(self, cli_sock, cli_host):
        room_id = str(self.Groom_num)
        self.Groom_num += 1
        game_room = Game_room(room_id, cli_sock, cli_host)
        self.Groom_list[room_id] = game_room
        req = {
            'room_id': str(room_id),
            'user_color': str(game_room.get_user1_color())
        }
        req = json.dumps(req)
        response = {
            'method': 'create',
            'req': req
        }
        response = json.dumps(response)
        cli_sock.sendall(response.encode("utf-8"))
    
    def join_room(self, cli_sock, cli_host, parm):
        response = {
            'method': 'join'
        }
        try:
            parm = json.loads(parm)
            room_id = str(parm['room_id'])
            
            if room_id in self.Groom_list.keys() and self.Groom_list[room_id].user2 != -1:
                self.Groom_list[room_id].add_user(cli_host)
                req = {
                    'room_id': str(room_id)
                }
                response['req'] = req
            else:
                response['req'] = "join error"
        except Exception as e:
            response['req'] = "input error"
            error(e)
        
        response = json.dumps(response)
        cli_sock.sendall(response.encode("utf-8"))
    
    def put_point(self, cli_sock, cli_host, parm):
        response = {
            'method': 'put'
        }
        response_2 = {
            'method': 'watch'
        }
        try:
            parm = json.loads(parm)
            room_id = str(parm['room_id'])
            point_location = str(parm['point_location'])
            
            if room_id in self.Groom_list.keys() and self.Groom_list[room_id].user2 != -1:
                game_room = self.Groom_list[room_id]
                user_color = game_room.get_users_color(cli_host)
                status = game_room.put_point(point_location, user_color)
                other_sock = game_room.get_other_user(user_host=cli_host)
                if status == 0:
                    response['req'] = 'input error'
                elif status == 1:
                    response['req'] = 'success'
                    response_2['req'] = 'success'
                    response_2 = json.dumps(response_2)
                    other_sock.send_all(response_2.encode("utf-8"))
                elif status == 2:
                    response['req'] = 'win'
                    response_2['req'] = 'lose'
                    response_2 = json.dumps(response_2)
                    other_sock.send_all(response_2.encode("utf-8"))
                    self.Groom_list.pop(room_id)
            else:
                response['req'] = "id error"
        except Exception as e:
            response['req'] = "input error"
            error(e)
        response = json.dumps(response)
        cli_sock.sendall(response.encode("utf-8"))


class Game_room(object):
    def __init__(self, room_id, user1_sock, user1_host):
        self.id = room_id
        self.user1 = user1_host
        self.user1_sock = user1_sock
        self.user2 = -1
        self.user2_sock = -1
        self.game = Gomoku_game()
        self.user1_color = random.randint(1, 2)
        self.user2_color = 1 if self.user1_color else 2
    
    def put_point(self, point, user_color):
        if not check_location(point) or self.user2 == -1:
            return 0
        return self.game.put_chess(point=point, point_type=user_color)
    
    def add_user(self, user2_sock, user2_host):
        self.user2 = user2_host
        self.user2_sock = user2_sock
    
    def get_user1_color(self):
        return self.user1_color
    
    def get_users_color(self, user_host):
        if user_host == self.user1:
            return self.user1_color
        elif user_host == self.user2:
            return self.user2_color
        else:
            return 0
    
    def get_other_user(self, user_host):
        return self.user1_sock if user_host == self.user2 else self.user2_sock


if __name__ == '__main__':
    s = Server()
    