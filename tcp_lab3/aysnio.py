#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/25'
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
import asyncio

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    while True:
        try:
            data = ""
            while True:
                recv_data = await reader.read(1)
                recv_data = recv_data.decode("utf-8")
                data += recv_data
                if "!" in recv_data:
                    break
            message = data
            
            print(f"Received {message!r} from {addr!r}")
            
            
            print(f"Send: {data!r}")
            writer.write(data.encode("utf-8"))
            await writer.drain()
        except Exception as e:
            print(e)

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())