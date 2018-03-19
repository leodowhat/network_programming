#_*_coding:utf-8_*_
'''
    author:zhanglin
'''

from socket import *

HOST = 'www.baidu.com'
PORT = 80
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

tcpCliSock.send(bytes('GET / \n', 'utf-8'))
data = tcpCliSock.recv(BUFSIZ)

with open(r'web_pages.txt', 'r+') as f:
    f.write(data.decode('utf-8'))
