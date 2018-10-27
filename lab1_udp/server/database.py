#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/16'
"""
import sqlite3
import json, random
import hashlib
import logging

logging.basicConfig(level=logging.INFO)


class database_init():
    """
    this class only for create database
    """
    
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        try:
            database_conn = sqlite3.connect('chatRoom.db')
            logging.info("Opened database successfully")
            database_conn.execute('''CREATE TABLE users_information(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(128) NOT NULL,
        password VARCHAR(128) NOT NULL,
        token VARCHAR(128) NOT NULL,
        friends TEXT,
        is_login INTEGER NOT NULL,
        ip VARCHAR(128) NOT NULL
      );
    ''')
            database_conn.commit()
            logging.info("user information table created successfully")
            database_conn.execute('''CREATE TABLE message(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_text TEXT,
        to_user INTEGER NOT NULL,
        from_user INTEGER NOT NULL,
        has_sent INTEGER NOT NULL
    );
    ''')
            logging.info("user information table created successfully")
            database_conn.commit()
            database_conn.close()
            logging.info('init the database success!')
        except Exception as e:
            logging.error("init the database error")


class database():
    """
    this class is connect from server to database,
    all of it depends on token
    """
    
    def __init__(self):
        """
        init database connect
        """
        try:
            self.database_conn = sqlite3.connect('chatRoom.db')
            logging.info("connect database succsss")
        except:
            logging.error("connect database error")
    
    def get_token(self, username, password):
        """
        selct user's token from username and password
        :param username:
        :param password:
        :return: token or False
        """
        user = self.database_conn.execute("SELECT username FROM users_information WHERE username=?", [username])
        if user.fetchall() == []:
            return False
        else:
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            token = self.database_conn.execute("SELECT token FROM users_information WHERE username=? AND password=?",
                                               [username, password]).fetchall()[0][0]
            return token
    
    def insert_user(self, username, password):
        """
        insert user from username and password
        :param username:
        :param password:
        :return: token or error
        """
        user = self.database_conn.execute("SELECT username FROM users_information WHERE username=?", [username])
        if user.fetchall() == []:
            friend = json.dumps([])
            random_str = str(int(random.random() * 10000000000)) + username + str(int(random.random() * 10000000000))
            token = hashlib.md5(random_str.encode('utf-8')).hexdigest()
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            ip = json.dumps(("0.0.0.0", 23333))
            self.database_conn.execute("INSERT INTO users_information VALUES (NULL,?,?,?,?,?,?)",
                                       [username, password, token, friend, 0, ip])
            
            return token
        else:
            return False
    
    def insert_frients(self, token, friend_id):
        user_id = self.database_conn.execute("SELECT id FROM users_information WHERE token=?", [token]).fetchall()
        if user_id == []:
            return "error"
        else:
            friends = \
            self.database_conn.execute("SELECT friends FROM users_information WHERE token=?", [token]).fetchall()[0][0]
            friends = json.loads(friends)
            friends.append(friend_id)
            friends = json.dumps(friends)
            self.database_conn.execute("UPDATE users_information SET friends=? WHERE token=?", [friends, token])
            self.database_conn.commit()
            return True
    
    def get_friends(self, token):
        """
        get friends by token
        :param token:
        :return: list of friends id or error
        """
        friends = self.database_conn.execute("SELECT friends FROM users_information WHERE token=?", [token]).fetchall()
        if friends == []:
            return False
        else:
            friends = json.loads(friends[0][0])
            return friends
    
    def login(self, token, ip):
        """
        update user's status about is_login and ip
        :param token:
        :param ip:
        :return: status
        """
        user = self.database_conn.execute("SELECT id from users_information WHERE token=?", [token]).fetchall()
        if user == []:
            return False
        else:
            ip = json.dumps(ip)
            self.database_conn.execute("UPDATE users_information SET is_login=1,ip=? WHERE token=?", [ip, token])
            self.database_conn.commit()
            return True
    
    def logout(self, token):
        """
        update user's status about is_login and ip
        :param token:
        :return:
        """
        user = self.database_conn.execute("SELECT id from users_information WHERE token=?", [token]).fetchall()
        if user == []:
            return False
        else:
            ip = json.dumps(("0.0.0.0", 23333))
            self.database_conn.execute("UPDATE users_information SET is_login=0,ip=? WHERE token=?", [ip, token])
            self.database_conn.commit()
            return True
    
    def get_message(self, token):
        """
        get messages when you haven't recive
        :param token:
        :return:
        """
        user_id = self.database_conn.execute("SELECT id from users_information WHERE token=?", [token]).fetchall()
        if user_id == []:
            return False
        else:
            messages_list = self.database_conn.execute(
                "SELECT id,message_text,has_sent,from_user FROM message WHERE to_user=?", user_id[0]).fetchall()
            messages = []
            for message in messages_list:
                if message[2] == 0:
                    messages.append([message[0], message[1], message[3]])
            return messages
    
    def sent_message(self, token, not_send_ids, send_ids, message):
        """
        this function for user to send message to haven't login user
        :param token:
        :param from_id:
        :param to_ids:
        :param message:
        :return:
        """
        user_id = self.database_conn.execute("SELECT id FROM users_information WHERE token=?", [token]).fetchall()
        if user_id == []:
            return False
        else:
            user_id = user_id[0][0]
            message = message.encode('utf-8')
            for to_id in not_send_ids:
                self.database_conn.execute("INSERT INTO message VALUES (NULL,?,?,?,?)", [message, to_id, user_id, 0])
            for to_id in send_ids:
                self.database_conn.execute("INSERT INTO message VALUES (NULL,?,?,?,?)", [message, to_id, user_id, 1])
            self.database_conn.commit()
            return True
    
    def update_message(self, message_id):
        try:
            self.database_conn.execute("UPDATE message SET has_sent=1 WHERE id=?", [message_id])
            self.database_conn.commit()
            return True
        except:
            return False
    
    def get_all_login_user(self):
        users = self.database_conn.execute("SELECT id,ip FROM users_information WHERE is_login=1").fetchall()
        return list(users)
    
    def get_user_status(self, user_id):
        users = self.database_conn.execute("SELECT is_login,ip FROM users_information WHERE id=?", [user_id]).fetchall()
        
        if users == []:
            return False
        else:
            is_login = users[0][0]
            addr = tuple(json.loads(users[0][1]))
            return is_login, addr
    
    def get_user_name(self, token):
        users = self.database_conn.execute("SELECT username FROM users_information WHERE token=?", [token]).fetchall()
        if users == []:
            return False
        else:
            return users[0][0]
    
    def get_id(self,token):
        users = self.database_conn.execute("SELECT id FROM users_information WHERE token=?", [token]).fetchall()
        if users == []:
            return False
        else:
            return users[0][0]
        
    def get_id_by_username(self,username):
        users = self.database_conn.execute("SELECT id FROM users_information WHERE username=?", [username]).fetchall()
        if users == []:
            return False
        else:
            return users[0][0]


# if __name__ == '__main__':
#     try:
#         database_init()
#     except:
#         logging.error("error in databases")
#     db = database()
#     token_user_1 = db.insert_user("ngc7293","123456")
#     logging.info("insert seccuss and user1's token is" + token_user_1)
#     ip = ("127.0.0.1",23333)
#     if db.login(token_user_1,ip) == True:
#         logging.info("login seccuss")
#     else:
#         logging.info("login error")
#     token_user_2 = db.insert_user("hammer","hammernb")
#     logging.info("insert seccuss and user2's token is" + token_user_2)
#     ip = ("127.0.0.1",23456)
#     if db.login(token_user_2,ip) == True:
#         logging.info("login seccuss")
#     else:
#         logging.info("login error")
#     friends_of_user1 = db.get_friends(token_user_1)
#     logging.info("friends of user1 is :")
#     logging.info(friends_of_user1)
#     db.insert_frients(token_user_1,2)
#     friends_of_user1 = db.get_friends(token_user_1)
#
#     logging.info("user's friends is ok")
#
#     db.logout(token_user_2)
#
#     logging.info("user2 is logout")
#
#     users = db.get_all_login_user()
#     logging.info("user login is:")
#     logging.info(users)
#
#     db.sent_message(token_user_1,[2],[],"hello world")
#
#     db.login(token_user_2,ip)
#     message = db.get_message(token_user_2)
#     logging.info(message)
#
#     db.logout(token_user_1)
#
#     logging.info("test is done")
#
if __name__ == '__main__':
    db = database()
    
    print(db.update_message(3))
