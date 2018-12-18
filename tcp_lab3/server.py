#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/21'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""

import socket
import argparse
import os
from multiprocessing import Process, Manager
import threading
import select
import queue
import asyncio


def send_file_server(cli_sock, file_path):
    file_path = os.getcwd() + '/test/' + file_path
    
    try:
        if not os.path.exists(file_path):
            send_data = b'don\'t have this file\r\n'
        else:
            file_size = os.path.getsize(file_path)
            cli_sock.sendall(str(file_size).encode("utf-8")+b'\r\n')
            with open(file_path, 'rb') as f:
                send_data = f.read()
        cli_sock.sendall(send_data)
    except Exception as e:
        print(e)


# this part is for single process server
def single_process_server(cli_list, path_list):
    while True:
        if cli_list:
            cli_sock = cli_list.pop()
            file_path = path_list.pop()
            send_file_server(cli_sock, file_path)
        else:
            continue


def sp_show_list(cli_list_list):
    while True:
        if cli_list_list:
            cli_sock = cli_list_list.pop()
            send_data = ""
            for file in os.listdir(os.getcwd() + '/test/'):
                send_data += "   " + file + "\n"
            send_data = send_data + "\r\n"
            send_data = send_data.encode("utf-8")
            cli_sock.sendall(send_data)
        else:
            continue


def single_process(single_ip, single_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((single_ip, single_port))
    server_sock.listen(1024)
    print(f'Serving on {single_ip,str(single_port)}')
    
    cli_list = Manager().list()
    path_list = Manager().list()
    cli_list_list = Manager().list()
    
    p = Process(target=single_process_server, args=(cli_list, path_list,))
    p2 = Process(target=sp_show_list, args=(cli_list_list,))
    p.start()
    p2.start()
    
    while True:
        cli_sock, cli_addr = server_sock.accept()
        data = ""
        flag = 0
        while True:
            recv_data = cli_sock.recv(1024).decode("utf-8")
            if "\r\n" in recv_data:
                data += recv_data
                break
            elif recv_data == "":
                flag = 1
                break
            else:
                data += recv_data
        
        if flag == 1:
            cli_sock.close()
            continue
        data = data[:-2]
        
        print(f"Received {data!r} from {cli_addr!r}")
        
        if data == "list":
            cli_list_list.append(cli_sock)
        else:
            file_path = data
            cli_list.append(cli_sock)
            path_list.append(file_path)


# this part for multi process server
def list_dir():
    data = ""
    for file in os.listdir(os.getcwd() + '/test/'):
        data += "   " + file + "\n"
    return data.encode("utf-8")


def multi_process_server(cli_sock):
    data = ""
    flag = 0
    while True:
        recv_data = cli_sock.recv(1024).decode("utf-8")
        if "\r\n" in recv_data:
            data += recv_data
            break
        elif recv_data == "":
            flag = 1
            break
        else:
            data += recv_data
            
        
    if flag == 1:
        cli_sock.shutdown(2)
        
    data = data[:-2]
    if data == "list":
        send_data = list_dir()
        cli_sock.sendall(send_data)
    else:
        file_path = data
        send_file_server(cli_sock, file_path)
    
    cli_sock.close()
    


def multi_process(multi_ip, mutli_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((multi_ip, mutli_port))
    server_sock.listen(1024)
    
    print(f'Serving on {multi_ip,str(mutli_port)}')
    
    while True:
        cli_sock, cli_addr = server_sock.accept()
        t = threading.Thread(target=multi_process_server, args=(cli_sock,))
        t.start()


# this part for select server
def get_file(file_path):
    if type(file_path) is bytes:
        file_path = file_path.decode("utf-8")
    file_path = os.getcwd() + '/test/' + file_path
    file_size = os.path.getsize(file_path)
    try:
        if not os.path.exists(file_path):
            send_data = b'don\'t have this file\r\n'
        else:
            with open(file_path, 'rb') as f:
                send_data = f.read()
        return str(file_size), send_data
    except Exception as e:
        print(e)


def select_server(select_ip, select_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((select_ip, select_port))
    print("server is bind in (" + str(select_ip) + " , " + str(select_port) + ")")
    server_sock.setblocking(False)
    server_sock.listen(1024)
    print("server is listening ...")
    
    inputs = [server_sock, ]
    outputs = []
    message_queue = {}
    
    while True:
        print("server is waiting events ...")
        readable, writeable, exceptional = select.select(inputs, outputs, inputs)
        
        for s in readable:
            
            if s is server_sock:
                cli_sock, cli_addr = server_sock.accept()
                print("new connection come from : " + str(cli_sock))
                
                cli_sock.setblocking(False)
                inputs.append(cli_sock)
                
                message_queue[cli_sock] = queue.Queue()
            
            else:
                data = b""
                flag = 0
                while True:
                    recv_data = s.recv(1024)
                    if not recv_data:
                        flag = 1
                    else:
                        data += recv_data
                        if b"\r\n" in recv_data:
                            break
                
                if flag == 1:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.shutdown(2)
                    del message_queue[s]
                
                else:
                    data = data[:-2].decode("utf-8")
                    print("recv data [%s] from %s" % (data, s.getpeername()[0]))
                    if data == "list":
                        send_data = list_dir()
                    else:
                        file_path = data
                        file_size, send_data = get_file(file_path)
                        file_size += '\r\n'
                        message_queue[s].put(file_size.encode("utf-8"))
                    send_data = send_data + b'\r\n'
                    message_queue[s].put(send_data)
                    if s not in outputs:
                        outputs.append(s)
        
        for s in writeable:
            try:
                next_message = message_queue[s].get_nowait()
            except queue.Empty:
                print('output queue for [%s] is empty' % s.getpeername()[0])
                outputs.remove(s)
            else:
                print('send %s to %s' % (next_message, s.getpeername()[0]))
                s.sendall(next_message)
        
        for s in exceptional:
            print('handling exceptional condition for', s.getpeername()[0])
            
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            
            del message_queue[s]


# this part for asyncio server

async def asyncio_server(reader, writer):
    addr = writer.get_extra_info('peername')
    while True:
        try:
            data = b""
            while True:
                recv_data = await reader.read(1)
                data += recv_data
                if b"\r\n" in data:
                    break
                if not data:
                    return
                recv_data = recv_data.decode("utf-8")
                print(f"Received {recv_data!r} from {addr!r}")
            
            data = data[:-2].decode("utf-8")
            
            if data == "list":
                send_data = list_dir()
            else:
                file_path = data
                file_size, send_data = get_file(file_path)
                file_size = file_size.encode("utf-8") + b'\r\n'
                writer.write(file_size)
            send_data += b'\r\n'
            
            print(f"Send: {send_data!r}")
            writer.write(send_data)
            await writer.drain()
        except Exception as e:
            print(e)


async def main(asy_ip, asy_port):
    
    server = await asyncio.start_server(
        asyncio_server, asy_ip, asy_port)
    
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('-p', '--port', default=23333, type=int)
    parser.add_argument('host',
                        help='an integer for the accumulator')
    parser.add_argument('-m', '--method', default="single_process",
                        choices=['single_process', 'mutil_process', 'select', 'asyncio'])
    args = parser.parse_args()
    
    ip = args.host
    port = int(args.port)
    method = args.method

    if method == "single_process":
        single_process(ip, port)
    elif method == "mutil_process":
        multi_process(ip, port)
    elif method == "select":
        select_server(ip, port)
    elif method == "asyncio":
        asyncio.run(main(ip, port))
        