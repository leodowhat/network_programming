#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Feb 27, 2016

@author: mountain
'''
import select
import socket
import sys
import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server_address = ('localhost', 1234)
server.bind(server_address)
server.listen(5)
print 'server is listening on %s port %s' % server_address
msg_queues = {}
timeout = 1000 * 60
#POLLIN: There is data to read
#POLLPRI: There is urgent data to read
#POLLOUT: Ready for output
#POLLERR: Error condition of some sort
#POLLHUP: Hung up
#POLLNVAL: Invalid request: descriptor not open
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
poller = select.poll()
#注册需要监听的事件
poller.register(server, READ_ONLY)
#文件描述符和socket映射
fd_to_socket = { server.fileno(): server}
while True:
     events = poller.poll(timeout)
     for fd, flag in events:
         sock = fd_to_socket[fd]
         if flag & (select.POLLIN | select.POLLPRI):
             if sock is server:
                 conn, client_address = sock.accept()
                 conn.setblocking(False)
                 fd_to_socket[conn.fileno()] = conn
                 poller.register(conn, READ_ONLY)
                 msg_queues[conn] = Queue.Queue()
             else:
                 data = sock.recv(1024)
                 if data:
                     msg_queues[sock].put(data)
                     poller.modify(sock, READ_WRITE)
                 else:
                     poller.unregister(sock)
                     sock.close()
                     del msg_queues[sock]
         elif flag & select.POLLHUP:
             poller.unregister(sock)
             sock.close()
             del msg_queues[sock]
         elif flag & select.POLLOUT:
             if not msg_queues[sock].empty():
                 msg = msg_queues[sock].get_nowait()
                 sock.send(msg)
             else:
                 poller.modify(sock, READ_ONLY)
         elif flag & select.POLLERR:
             poller.unregister(sock)
             sock.close()
             del msg_queues[sock]

作者：MountainKing
链接：https://www.jianshu.com/p/1020c11f016c
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。