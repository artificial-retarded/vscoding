import socket
import threading
import time
from time import sleep, ctime

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(("10.62.63.145", 5438))
#sk.bind(("xxx.xxx.xx.xx",xxxx))
sk.listen(5)

print("sever listening 5438, maximum connection 5")

def commu(conn,address):
    buf=conn.recv(2048)
    print(buf)
    if buf == b'hello 123 nihao':
            bs = str(buf, encoding="utf8")
            print('welcome to server!')
            print(bs)
            print(bs.split())
    #后续数据处理
    conn.send(bytes(bs[1],encoding="utf8"))


while True:    
    conn, address = sk.accept()
    print(address)
    print(conn)
    thread=threading.Thread(target=commu, args=(conn,address))
    thread.start()