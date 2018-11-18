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
import random

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

Gomoku, also called Five in a Row, is an abstract strategy board game. It is traditionally played with Go pieces (black and white stones) on a Go board, using 15×15 of the 19×19 grid intersections.[1] Because pieces are not moved or removed from the board, Gomoku may also be played as a paper and pencil game. The game is known in several countries under different names.

Players alternate turns placing a stone of their color on an empty intersection. The winner is the first player to form an unbroken chain of five stones horizontally, vertically, or diagonally.

start game for input s!
"""

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
              
congratulation you win ! if you want to restart this game please input r,\
if you want to exit please input e.                
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

it's so bad that you lose ! if you want to restart this game please input r,\
if you want to exit please input e.
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
    def __init__(self, user1_sock):
        self.board = init_board()
        self.dirc = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]

        self.user1 = user1_sock
        self.user2 = -1

        self.user1_color = random.choices([BLACK, WHITE])
        self.user2_color = BLACK if self.user1_color == WHITE else WHITE

    def join_game(self, user2_sock):
        self.user2 = user2_sock

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
        for discs in DIRC:
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


class server(object):
    def __init__(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(ADDR)
        self.server_sock.listen(AC_CLIENT)

        self.wait_game_list = []
        self.run_game_list = []

    def do_accept(self):
        while True:
            try:
                client_sock, client_addr = self.server_sock.accept()
            except Exception as e:
                print(e)

    def create_game(self, user_sock):
        game = gomoke(user_sock)
        self.wait_game_list.append(game)

    def join_game(self, user_sock, game):
        game.join_game(user_sock)
        self.run_game_list.append(game)
        self.wait_game_list.remove(game)

    def do_recv(self, client_sock):
        while True:





if __name__ == '__main__':
    a = board()
    print(a.show_board())
