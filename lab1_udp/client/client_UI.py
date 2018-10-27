#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/19'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from client import client

from multiprocessing import Process

import chat, login

class MainWindow(QMainWindow, chat.Ui_MainWindow):
    """
    the class of main windows
    user must login or register success
    """
    def __init__(self, parents=None):
        super(MainWindow, self).__init__(parents)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send_message)
        
    
    def set_connect(self, client):
        self.client = client
    
    def send_message(self):
        to_user = self.textEdit_2.toPlainText()
        message = self.textEdit_3.toPlainText()
        if message != "" and to_user != "":
            try:
                
                self.client.send_message(message, self.client.token, to_user)
                show_text = "To {0} : {1}".format(str(to_user),message)
                self.listWidget.addItem(show_text)
                
            except:
                self.textEdit_3.setText("error to send message")
        else:
                self.textEdit_3.setText("error to send")
        

    def resvmessage(self,recv_data):
        if "message" in recv_data:
            message = recv_data["message"]
            from_id = recv_data["from_user"]
            show_text = "From {0} : {1}".format(str(from_id),message)
            self.listWidget.addItem(show_text)
        else:
            status = recv_data["status"]
            show_text = "logging : {0}".format(status)
            self.listWidget.addItem(show_text)
        

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,'本程序',"是否要退出程序？",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.client.log_out()
            event.accept()
        else:
            event.ignore()
        
        
class logindialog(QDialog, login.Ui_Dialog):
    def __init__(self, parents=None):
        super(logindialog, self).__init__(parents)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)
    
    def set_connect(self, client):
        self.client = client
    
    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username == "" or password == "":
            self.label_4.setText("login error")
        else:
            status = self.client.login(username,password)
            if status == True:
                self.accept()
            else:
                self.label_4.setText("login error")
    
    def register(self):
        username = self.lineEdit.text()
        password = self.lineEdit.text()
        if username == "" or password == "":
            self.label_4.setText("register error")
        else:
            status = self.client.register(username,password)
            if status == True:
                self.accept()
            else:
                self.label_4.setText("register error")
            
            
class WorkTread(QThread):
    recv_data = pyqtSignal(object)
    
    def __init__(self,conn):
        super(WorkTread,self).__init__()
        self.c_conn = conn
        
    def run(self):
        while True:
            response = self.c_conn.recv_message()
            if response == False:
                continue
            else:
                self.recv_data.emit(response)
                
        
    

def main():
    app = QApplication(sys.argv)
    c_conn = client()
    dialog = logindialog()
    dialog.set_connect(c_conn)
    if dialog.exec_() == QDialog.Accepted:
        the_window = MainWindow()
        the_window.set_connect(c_conn)
        recv_data = WorkTread(c_conn)
        recv_data.recv_data.connect(the_window.resvmessage)
        recv_data.start()
        the_window.show()
        sys.exit(app.exec_())
    
    
        
if __name__ == "__main__":
    main()