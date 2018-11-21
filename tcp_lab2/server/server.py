#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'
"""
from multiprocessing import Process, Manager
from socket import *

HOST = "0.0.0.0"
PORT = 23333
AC_CLIENT = 1024
ADDR = (HOST, PORT)

START_TXT = """
                     __                                     
                    /  |                                    
  ______    ______  $$ |____    ______   _______    ______  
 /      \  /      \ $$      \  /      \ /       \  /      \ 
/$$$$$$  |/$$$$$$  |$$$$$$$  | $$$$$$  |$$$$$$$  |/$$$$$$  |
$$ |  $$ |$$ |  $$ |$$ |  $$ | /    $$ |$$ |  $$ |$$ |  $$ |
$$ \__$$ |$$ \__$$ |$$ |__$$ |/$$$$$$$ |$$ |  $$ |$$ \__$$ |
$$    $$ |$$    $$/ $$    $$/ $$    $$ |$$ |  $$ |$$    $$ |
 $$$$$$$ | $$$$$$/  $$$$$$$/   $$$$$$$/ $$/   $$/  $$$$$$$ |
/  \__$$ |                                        /  \__$$ |
$$    $$/                                         $$    $$/ 
 $$$$$$/                                           $$$$$$/
 
this is a gobang game and if you want to start your game please input s!
if you want to read some hint for this game you can input h!
enjoy yourself!\n
"""

HINT_TXT = """

Gomoku, also called Five in a Row, is an abstract strategy board game. It is traditionally played with Go pieces (
black and white stones) on a Go board, using 15×15 of the 19×19 grid intersections.[1] Because pieces are not moved
or removed from the board, Gomoku may also be played as a paper and pencil game. The game is known in several
countries under different names.

Players alternate turns placing a stone of their color on an empty intersection. The winner is the first player to
form an unbroken chain of five stones horizontally, vertically, or diagonally.

start game for input s!\n
"""

WAIT_TXT = """
please wait people to start a game...\n
"""

START_GAME_TXT = """
will start a game , your color is {}
"""

TURN_TXT = "it's your trun to put chess please input as \"p xx xx!\" to put chess: "

NOT_TURN_TXT = "please wait other to put chess! \n"

WIN_TEXT = """
                                                   /$$          
                                                  |__/          
 /$$   /$$  /$$$$$$  /$$   /$$       /$$  /$$  /$$ /$$ /$$$$$$$ 
| $$  | $$ /$$__  $$| $$  | $$      | $$ | $$ | $$| $$| $$__  $$
| $$  | $$| $$  \ $$| $$  | $$      | $$ | $$ | $$| $$| $$  \ $$
| $$  | $$| $$  | $$| $$  | $$      | $$ | $$ | $$| $$| $$  | $$
|  $$$$$$$|  $$$$$$/|  $$$$$$/      |  $$$$$/$$$$/| $$| $$  | $$
 \____  $$ \______/  \______/        \_____/\___/ |__/|__/  |__/
 /$$  | $$                                                      
|  $$$$$$/                                                      
 \______/                                                       
              
congratulation you win ! if you want to restart this game please input s!,\
if you want to exit please input e!.\n
"""

LOSE_TEXT = """

                                     __                               
                                    /  |                              
 __    __   ______   __    __       $$ |  ______    _______   ______  
/  |  /  | /      \ /  |  /  |      $$ | /      \  /       | /      \ 
$$ |  $$ |/$$$$$$  |$$ |  $$ |      $$ |/$$$$$$  |/$$$$$$$/ /$$$$$$  |
$$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |$$ |  $$ |$$      \ $$    $$ |
$$ \__$$ |$$ \__$$ |$$ \__$$ |      $$ |$$ \__$$ | $$$$$$  |$$$$$$$$/ 
$$    $$ |$$    $$/ $$    $$/       $$ |$$    $$/ /     $$/ $$       |
 $$$$$$$ | $$$$$$/   $$$$$$/        $$/  $$$$$$/  $$$$$$$/   $$$$$$$/ 
/  \__$$ |                                                            
$$    $$/                                                             
 $$$$$$/                                                              

it's so bad that you lose ! if you want to restart this game please input s!,
if you want to exit please input e!.\n
"""
EMPTY = 0
BLACK = 1
WHITE = 2


def init_board():
    return [[EMPTY for i in range(15)] for j in range(15)]


def check_location(point):
    x = point[0]
    y = point[1]
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    else:
        return True


def get_next_location(point, dirc):
    x = point[0] + dirc[0]
    y = point[1] + dirc[1]
    return x, y


class gomoke(object):
    def __init__(self, user1_cli_sock, user2_cli_sock):
        self.board = init_board()
        self.dirc = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]
        
        self.users = [user1_cli_sock, user2_cli_sock]
        self.users_color = [BLACK, WHITE]
    
    def show_board(self):
        show_text = ""
        for rows in self.board:
            for point in rows:
                if point == 0:
                    show_text += "0"
                elif point == 1:
                    show_text += "+"
                elif point == 2:
                    show_text += "-"
                show_text += " "
            show_text += "\n"
        return show_text
    
    def check_win(self, point):
        x, y = point
        point_type = self.board[x][y]
        for discs in self.dirc:
            count = 1
            for dirc in discs:
                x, y = point
                while True:
                    if not get_next_location((x, y), dirc):
                        break
                    x, y = get_next_location((x, y), dirc)
                    if self.board[x][y] == point_type:
                        count += 1
                    else:
                        break
            if count == 5:
                return True
        else:
            return False
    
    def put_chess(self, point, point_type):
        x, y = point
        if self.board[x][y] != EMPTY or check_location(point) == False and point_type not in [BLACK, WHITE, EMPTY]:
            return 0
        else:
            self.board[x][y] = point_type
            if self.check_win(point):
                return 2
            else:
                return 1
    
    def run(self):
        do_user = 0
        other_user = 1
        recv_data = ""
        for i in range(2):
            send_text = self.show_board()
            send_text += TURN_TXT if i == do_user else NOT_TURN_TXT
            self.users[i].sendall(send_text.encode("utf-8"))
        while True:
            try:
                data = self.users[do_user].recv(1024).decode("utf-8")
                if "!" not in data:
                    recv_data += data
                    continue
                else:
                    recv_data += data
                    recv_data = recv_data.rstrip("\n")
                    recv_data = recv_data.rstrip("!")
                    way, x, y = recv_data.split(" ")
                    x = int(x)
                    y = int(y)
                    if check_location((x, y)):
                        status = self.put_chess((x, y), self.users_color[do_user])
                        if status == 0:
                            raise Exception("input error")
                        elif status == 1:
                            send_text = self.show_board()
                            do_send_text = send_text + NOT_TURN_TXT
                            not_do_send_text = send_text + TURN_TXT
                            self.users[do_user].sendall(do_send_text.encode("utf-8"))
                            self.users[other_user].sendall(not_do_send_text.encode("utf-8"))
                            do_user, other_user = other_user, do_user
                        elif status == 2:
                            send_text = self.show_board()
                            do_send_text = send_text + WIN_TEXT
                            not_do_send_text = send_text + LOSE_TEXT
                            self.users[do_user].sendall(do_send_text.encode("utf-8"))
                            self.users[other_user].sendall(not_do_send_text.encode("utf-8"))
                            do_user, other_user = other_user, do_user
                            return 0
                    else:
                        raise Exception("input error")
                    recv_data = ""
            except Exception as e:
                send_text = "your input is error, please reinput something:".encode("utf-8")
                self.users[do_user].sendall(send_text)
                print(e)
                recv_data = ""


class server(object):
    def __init__(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(ADDR)
        self.server_sock.listen(AC_CLIENT)
        
        self.wait_user_list = Manager().list()
        self.user_list = Manager().list()
        self.user_list_status = Manager().list()
        print("start listening "+str(ADDR))
    
    def do_accept(self):
        index = 0
        while True:
            try:
                client_sock, client_addr = self.server_sock.accept()
                print("accepting " + str(client_addr))
                self.user_list_status.append(0)
                self.user_list.append(client_sock)
                p = Process(target=self.do_recv, args=(client_sock, self.wait_user_list, index, self.user_list, self.user_list_status))
                
                p.start()
                index += 1
            except Exception as e:
                print(e)
    
    def do_recv(self, cli_sock, wait_user_list, user_index, user_list, user_list_status):
        send_data = START_TXT
        cli_sock.sendall(send_data.encode("utf-8"))
        recv_data = ""
        while True:
            try:
                data = cli_sock.recv(1024).decode("utf-8")
                if data == "":
                    continue
                print("client send" + str(data))
                if "!" not in data:
                    recv_data += data
                    continue
                else:
                    recv_data += data
                    if "s" in recv_data:
                        if len(wait_user_list) == 0:
                            send_data = WAIT_TXT
                            cli_sock.sendall(send_data.encode("utf-8"))
                            
                            wait_user_list.append(user_index)
                            user_list_status[user_index] = 0
                            
                            while True:
                                if user_list[user_index] == 1:
                                    user_list[user_index] = 0
                                    break
                        else:
                            other_user_id = wait_user_list.pop()
                            other_user = user_list[other_user_id]
                            gomoke(user1_cli_sock=other_user, user2_cli_sock=cli_sock).run()
                            user_list[other_user_id] = 1
                    elif "h" in recv_data:
                        send_data = HINT_TXT.encode("utf-8")
                        cli_sock.sendall(send_data)
                    else:
                        break
                recv_data = ""
            except Exception as e:
                print(e)
        cli_sock.shutdown(2)


if __name__ == '__main__':
    server().do_accept()
