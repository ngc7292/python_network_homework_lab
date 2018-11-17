#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/6'
"""

import random

class poker_game():
    def __init__(self):
        """
        init the game
        poker as "x-x",the 1st x is color and next x is number
        """
        self.poker = self.wash_poker()
        
        
    def wash_poker(self):
        """
        洗牌，返回乱序的扑克牌顺序
        :return:
        """
        color = ["1","2","3","4"]
        number = ["A","2","3","4","5","6","7","8","9","X","J","Q","K"]
        poker = []
        for i in color:
            for j in number:
                poker.append(i+"-"+j)
                
        poker.append("0-L")
        poker.append("0-S")
        random.shuffle(poker)
        return poker
    
    def distribute_poker(self):
        """
        发牌，返回三位玩家的牌，以及地主的位置
        :return: list
        """
        last_poker = self.poker[-3:]
        
        landlord_poker = random.sample(self.poker[:-3],1)[0]
        
        player1_poker = self.poker[0:-1:3]
        player2_poker = self.poker[1:-2:3]
        player3_poker = self.poker[2:-3:3]
        
        if landlord_poker in player1_poker:
            return [player1_poker+last_poker, player2_poker, player3_poker, 1]
        elif landlord_poker in player2_poker:
            return [player1_poker, player2_poker+last_poker, player3_poker, 2]
        elif landlord_poker in player3_poker:
            return [player1_poker, player2_poker, player3_poker+last_poker, 3]
        else:
            return False
        
    
    def check_poker(self,table_poker,player_poker):
        """
        整个游戏的判断逻辑，table_poker为桌上的牌，player_poker是玩家的牌,若玩家胜利，则返回True，若玩家失败，返回False
        :param table_poker: list
        :param player_poker: list
        :return: bool
        """
        pass
    
    def sort_poker(self,poker):
        """
        对所给的扑克牌排序
        :param poker: list
        :return: list
        """
        behind_poker = []
        other = []
        for i in poker:
            s = i.split("-")[0]
            
            
        
            
    def get_poker_type(self,poker):
        """
        获取出的牌的种类，包括0 王炸，1 炸，2 一个，3 顺子，4 一对，5 连对，6 三代一，7 飞机，8四带二
        :param poker: list
        :return: int
        """
        f_poker = ["A","2","3","4","5","6","7","8","9","X","J","Q","K","S","L"]
        s_poker = ["AA","22","33","44","55","66","77","88","99","XX","JJ","QQ","KK"]
        t_poker = ["AAA","222","333","444","555","666","777","888","999","XXX","JJJ","QQQ","KKK"]
        ft_poker = ["AAAA","2222","3333","4444","5555","6666","7777","8888","9999","XXXX","JJJJ","QQQQ","KKKK"]
        pass
        
        
        

    def end_game(self):
        pass


class player():
    def __init__(self,poker,is_land_lord):
        self.owner_poker = poker
        self.remind_poker = poker
        
        
if __name__ == '__main__':
    game = poker_game()
    print(game.distribute_poker())
        
        
    