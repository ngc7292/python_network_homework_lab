#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
EMPTY = 0
BLACK = 1
WHITE = 2


def set_board():
    return [[EMPTY for i in range(15)] for j in range(15)]


def check_location(point, dirc):
    x = point[0] + dirc[0]
    y = point[1] + dirc[1]
    if x < 0 or x >= 15 or y < 0 or y >= 15:
        return False
    else:
        return True


class board(object):
    def __init__(self):
        self.__board = set_board()

    def board(self):
        return self.__board

    def set_status(self, x, y, status):
        self.__board[x][y] = status

    def get_status(self, x, y):
        return self.__board[x][y]

    def reset(self):
        self.__board = board()
