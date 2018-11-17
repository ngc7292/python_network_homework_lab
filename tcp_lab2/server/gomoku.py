#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/12'

"""
EMPTY = 0
BLACK = 1
WHITE = 2

DIRC = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, -1), (1, 1)], [(-1, 1), (1, -1)]]


def get_next_location(point, dirc):
    x, y = point
    next_x, next_y = dirc
    x, y = x + next_x, y + next_y
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    else:
        return x, y


def check_location(point):
    x, y = point
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    else:
        return True


class Gomoku_game(object):
    
    def __init__(self):
        """
        init all game
        """
        self.board = self.init_board
    
    @property
    def init_board(self):
        return [[EMPTY for row in range(15)] for col in range(15)]
    
    def check_win(self, point):
        x, y = point
        point_type = self.board[x][y]
        for dircs in DIRC:
            count = 1
            for dirc in dircs:
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
    
    def reset(self):
        self.board = self.init_board


if __name__ == '__main__':
    test_game = Gomoku_game()
    test_game.put_chess((0, 0), BLACK)
    test_game.put_chess((0, 1), WHITE)
    test_game.put_chess((1, 0), BLACK)
    test_game.put_chess((2, 0), BLACK)
    test_game.put_chess((3, 0), BLACK)
    check = test_game.put_chess((4, 0), BLACK)
    print(check)
