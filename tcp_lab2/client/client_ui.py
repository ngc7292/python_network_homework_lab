#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/13'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.

"""
import PyQt5
from PyQt5.QtWidgets import QLabel
from .board import board

WIDTH = 540
HEIGHT = 540
MARGIN = 22
GRID = (WIDTH - 2 * MARGIN) / (15 - 1)
PIECE = 34
EMPTY = 0
BLACK = 1
WHITE = 2


class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()

class