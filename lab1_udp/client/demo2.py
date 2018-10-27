#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import chat,login
################################################
#######创建主窗口
################################################
class MainWindow(QMainWindow,chat.Ui_MainWindow):
    def __init__(self,parents=None):
        super(MainWindow ,self).__init__(parents)
        self.setupUi(self)
        
    def get_connect(self,conn):
        self.conn = conn
        
    def send_message(self):
        pass



################################################
#######对话框
################################################
class logindialog(QDialog,login.Ui_Dialog):
    def __init__(self,parents=None):
        super(logindialog ,self).__init__(parents)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)
        
    def get_connect(self,conn):
        self.conn = conn
        
    def login(self):
        self.accept()
    
    def register(self):
        self.label.setText("error!! ")
    
        




################################################
#######程序入门
################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog()
    if  dialog.exec_()==QDialog.Accepted:
        the_window = MainWindow()
        the_window.show()
        sys.exit(app.exec_())

