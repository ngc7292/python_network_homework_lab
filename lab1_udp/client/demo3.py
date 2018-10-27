#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time


class Backend(QThread):
    update_date = pyqtSignal()
    
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            self.update_date.emit(str(data))
            time.sleep(1)


class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)
    
    def handleDisplay(self, data):
        self.input.setText(data)


if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    b = Backend()
    w = Window()
    b.update_date.connect(w.handleDisplay)
    b.start()
    w.show()
    app.exec_()
