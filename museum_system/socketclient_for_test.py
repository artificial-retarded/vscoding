import socket 
import threading
import time

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("192.168.1.100",5437))
flag='hello'
while True:
    time.sleep(5)
    sock.send(b'hello 123 nihao')
    
    buf=sock.recv(2048)
    bs = str(buf, encoding="utf8")
    print('welcome to server!')
    print(bs)


sock.close()