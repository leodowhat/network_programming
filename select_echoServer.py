#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Feb 16, 2016

@author: mountain
'''
import socket
import select
from Queue import Queue

#AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。
#SOCK_STREAM指定使用面向流的TCP协议，如果要使用面向数据包的UCP协议，就指定SOCK_DGRAM。
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
#设置监听的ip和port
server_address = ('localhost', 1234)
server.bind(server_address)
#设置backlog为5，client向server发起connect，server accept后建立长连接，
#backlog指定排队等待server accept的连接数量，超过这个数量，server将拒绝连接。
server.listen(5)
#注册在socket上的读事件
inputs = [server]
#注册在socket上的写事件
outputs = []
#注册在socket上的异常事件
exceptions = []
#每个socket有一个发送消息的队列
msg_queues = {}
print "server is listening on %s:%s." % server_address
while inputs:
     #第四个参数是timeout，可选，表示n秒内没有任何事件通知，就执行下面代码
     readable, writable, exceptional = select.select(inputs, outputs, exceptions)
     for sock in readable:
         #client向server发起connect也是读事件，server accept后产生socket加入读队列中
         if sock is server:
             conn, addr = sock.accept()
             conn.setblocking(False)
             inputs.append(conn)
             msg_queues[conn] = Queue()
             print "server accepts a conn."
         else:
             #读取client发过来的数据，最多读取1k byte。
             data = sock.recv(1024)
             #将收到的数据返回给client
             if data:
                 msg_queues[sock].put(data)
                 if sock not in outputs:
                     #下次select的时候会触发写事件通知，写和读事件不太一样，前者是可写就会触发事件，并不一定要真的去写
                     outputs.append(sock)
             else:
                 #client传过来的消息为空，说明已断开连接
                 print "server closes a conn."
                 if sock in outputs:
                     outputs.remove(sock)
                 inputs.remove(sock)
                 sock.close()
                 del msg_queues[sock]
     for sock in writable:
         if not msg_queues[sock].empty():
             sock.send(msg_queues[sock].get_nowait())
         if msg_queues[sock].empty():
             outputs.remove(sock)
     for sock in exceptional:
         inputs.remove(sock)
         if sock in outputs:
             outputs.remove(sock)
         sock.close()
         del msg_queues[sock]

作者：MountainKing
链接：https://www.jianshu.com/p/1020c11f016c
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。