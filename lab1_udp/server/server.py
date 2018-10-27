#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/16'
__filename__ = 'server.py'
"""
import socket
import logging
import json

from multiprocessing import Process
from database import database

logging.basicConfig(level=logging.INFO)

MAX_SIZE = 1024

# connect_users = {}

class servers():
    def __init__(self):
        global MAX_SIZE
        ip = "127.0.0.1"
        port = 23333
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((ip, port))
        
        self.db = database()
        
        logging.info("socket create success")
        logging.info("bind hostname is (" + ip + "," + str(port) + ")")
        
        self.connect_users = {}
        
        self.server_listen()
    
    def server_listen(self):
        while True:
            try:
                logging.info("program is listening...")
                recv_data, addr = self.server_socket.recvfrom(MAX_SIZE)
                logging.info("recv the data from " + str(addr))
                # p = Process(target=self.do_recvdata, args=(recv_data, addr))
                # p.start()
                self.do_recvdata(recv_data,addr)
            except Exception as e:
                print(e)
    
    def do_recvdata(self, recv_data, addr):
        # global connect_users
        data = self.trans_request(recv_data)
        if data["method"] == "logout":
            token = data["parm"]["token"]
            status = self.logout(token)
            return status
        elif data["method"] == "send":
            token = data["parm"]["token"]
            message = data["parm"]["message"]
            to_user = data["parm"]["to_user"]
            from_name = self.get_name(token)
            if to_user == "all" and from_name != False:
                status = self.send_all_message(token,message)
                response_data = {
                    "status": "send seccuss",
                }
                response_data = json.dumps(response_data).encode("utf-8")
                self.server_socket.sendto(response_data, addr)
            elif to_user in self.connect_users and from_name != False:
                to_id = self.connect_users[to_user][0]
                # addr = self.connect_users[to_user][1]
                status = self.send_message(token, message, to_user, from_name)
                response_data = {
                    "status": "send seccuss",
                }
                response_data = json.dumps(response_data).encode("utf-8")
                self.server_socket.sendto(response_data, addr)
                return True
            else:
                response_data = {
                    "status": "send error",
                }
                response_data = json.dumps(response_data).encode("utf-8")
                self.server_socket.sendto(response_data, addr)
                return False
        elif data["method"] == "login" or data["method"] == "register":
            if data["method"] == "login":
                username = data["parm"]["username"]
                password = data["parm"]["password"]
                status = self.login(username, password, addr)
            elif data["method"] == "register":
                username = data["parm"]["username"]
                password = data["parm"]["password"]
                status = self.register(username, password, addr)
            else:
                status = False
            if status != False:
                token = status
                send_data = {
                    "status": "success",
                    "token": token
                }
                id = self.get_id(token)
                username = data["parm"]["username"]
                send_data = json.dumps(send_data).encode("utf-8")
                self.server_socket.sendto(send_data, addr)
                self.connect_users[username] = [id,addr]
                # messages = self.get_message_not_send(token)
                # for message in messages:
                #     message_id = message[0]
                #     from_id = message[2]
                #     send_data = {
                #         "from_id": from_id,
                #         "message": message[1].decode("utf-8")
                #     }
                #     send_data = json.dumps(send_data).encode("utf-8")
                #     self.server_socket.sendto(send_data, addr)
                #     self.update_message(message_id)
            else:
                send_data = {
                    "status": "error"
                }
                send_data = json.dumps(send_data).encode("utf-8")
                self.server_socket.sendto(send_data, addr)
            return True
    
    def get_id(self,token):
        return self.db.get_id(token)
    
    def get_name(self, token):
        """
        get id by token
        :param token:
        :return:
        """
        return self.db.get_user_name(token)
    
    def login(self, username, password, addr):
        """
        login by username and password
        :param username:
        :param password:
        :param addr:
        :return: token or FALSE
        """
        try:
            token = self.db.get_token(username, password)
            self.db.login(token, addr)
            return token
        except:
            return False
    
    def register(self, username, password, addr):
        """
        register by username and password
        :param username:
        :param password:
        :param addr:
        :return: token or FALSE
        """
        try:
            token = self.db.insert_user(username, password)
            self.db.login(token, addr)
            return token
        except:
            return False
    
    def logout(self, token):
        """
        logout user's status
        :param token:
        :return:
        """
        try:
            self.db.logout(token)
            username = self.get_name(token)
            self.connect_users.pop(username)
            return True
        except:
            return False
    
    def trans_request(self, data):
        """
        json loads the data which be recv
        :param data: bytes
        :return: dict
        """
        data = data.decode("utf-8")
        return json.loads(data)
    
    def get_message_not_send(self, token):
        """
        get message by token
        :param token:
        :return: list
        """
        return self.db.get_message(token)
    
    def send_message(self, token, message, to_user, from_user):
        """
        this function for send message
        :param token: string
        :param message: string
        :param to_id: int
        :param from_id: int
        :return: bool
        """
        to_id = self.connect_users[to_user][0]
        is_login, addr = self.db.get_user_status(to_id)
        send_ids = []
        not_send_ids = []
        if is_login == 1:
            send_data = {
                "from_user": from_user,
                "message": message,
            }
            send_data = json.dumps(send_data).encode("utf-8")
            self.server_socket.sendto(send_data, addr)
            send_ids.append(to_id)
        else:
            not_send_ids.append(to_id)
        return self.db.sent_message(token, not_send_ids, send_ids, message)
    
    def send_all_message(self,token,message):
        username = self.get_name(token)
        for user in self.connect_users:
            if user == username:
                continue
            else:
                self.send_message(token,message,user,username)
        return True
        
        
    def update_message(self, message_id):
        return self.db.update_message(message_id)


if __name__ == '__main__':
    servers()
