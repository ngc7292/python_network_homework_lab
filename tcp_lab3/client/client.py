#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/26'
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
import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='file download client')
    
    parser.add_argument('-p', '--port', default=23333, type=int)
    parser.add_argument('host',
                        help='input the ip')
    parser.add_argument('-m', '--method', default="list", choices=["list", "download"])
    parser.add_argument('-f', '--filename')
    parser.add_argument('-l', '--localfile')
    args = parser.parse_args()
    
    ip = args.host
    port = int(args.port)
    file_name = args.filename
    local_path = "recv/" + args.localfile
    method = args.method
    
    
    cli_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cli_sock.connect((ip, port))
    
    if method == "list":
        cli_sock.sendall("list\r\n".encode("utf-8"))
        recv_data = cli_sock.recv(1024)
        print(recv_data.decode("utf-8"))
        cli_sock.close()
    else:
        cli_sock.sendall(file_name.encode("utf-8")+b"\r\n")
        data = b""
        flag = 0
        while True:
            recv_data = cli_sock.recv(1024)
            data += recv_data
            if b"\r\n" in recv_data:
                break
            if not recv_data:
                flag = 1
                break
        print(data)
        if b"don't have this file\r\n" in data:
            print("don\'t have this file")
        else:
            file_size = int(data[:-2].decode("utf-8"))
            file_data = b""
            while True:
                recv_data = cli_sock.recv(65536)
                recv_length = len(recv_data)
                file_data += recv_data
                file_size -= recv_length
                if file_size <= 0:
                    break
            with open(local_path, 'wb') as f:
                f.write(file_data)
        cli_sock.close()
    
        