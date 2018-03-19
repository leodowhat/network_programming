#!/usr/bin/python

'test TCP server'

from socket import *
from time import ctime
import threading    #多线程模块
import re     #正则表达式模块

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

def Deal(sock, user):
	while True:
		data = sock.recv(BUFSIZ)    #接收用户的数据
		if data == 'quit':    #用户退出
			del clients[user]
			sock.send(data)
			sock.close()
			print '%s logout' %user
			break
		elif re.match('to:.+', data) is not None:    #选择通信对象
			data = data[3:]
			if clients.has_key(data):
				chatwith[sock] = clients[data]
				chatwith[clients[data]] = sock
			else:
				sock.send('the user %s is not exist' %data)
		else:
			if chatwith.has_key(sock):    #进行通信
				chatwith[sock].send("[%s] %s: %s" %(ctime(), user, data))
			else:
				sock.send('Please input the user who you want to chat with')


tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

clients = {}    #提供 用户名->socket 映射
chatwith = {}    #提供通信双方映射

while True:
	print 'waiting for connection...'
	tcpCliSock, addr = tcpSerSock.accept()
	print '...connected from:',addr
	username = tcpCliSock.recv(BUFSIZ)    #接收用户名
	print 'The username is:',username
	if clients.has_key(username):    #查找用户名
		tcpCliSock.send("Reuse")    #用户名已存在
		tcpCliSock.close()
	else:
		tcpCliSock.send("Welcome!")    #登入成功
		clients[username] = tcpCliSock
		chat = threading.Thread(target = Deal, args = (tcpCliSock,username))    #创建新线程进行处理
		chat.start()    #启动线程
tcpSerSock.close()