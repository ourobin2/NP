
import socket
import time ###########bug: login 和 whoami 全域變數問題
import sqlite3
import sys
 
clients = []  # 儲存用戶端socket物件的列表變數
HOST = 'localhost'
PORT = int(sys.argv[1])
s = socket.socket()
s.bind((HOST, PORT))
s.setblocking(False)  # 將此socket設成非阻塞
s.listen(15)
print('{} socket binded to {}'.format(HOST, PORT))


username = []
password = []
Login = []
#dic = {}
i=-1
while True:
    try:
        c, addr = s.accept()
        print('Got connection from{}:{}'.format(addr[0], addr[1]))
        # 也把跟用戶端連線的socket設成「非阻塞」
        c.setblocking(False) 
        # 將此用戶端socket物件存入clients列表備用
        clients.append(c)
        Login.append(0)
        c.send(b"\n********************************\n** Welcome to the BBS server. **\n********************************\n") 
        c.send(b"% ")
        
    except:
        pass  # 不理會錯誤
 
    # 逐一處理clients列表裡的每個用戶端socket…

    for c in clients:
        i+=1
        i=i%len(clients)

        try:
            
            data = c.recv(1024)
            data = data.decode()
            data = data.split()
            if data[0]=="exit" and len(data)==1:
                c.close()
                clients.remove(c)
                break
            elif data[0]=="register":
                if len(data)==4:
                    checkuser = 0
                    for i in range(len(username)):
                        if data[1]==username[i]:
                            checkuser=1
                    if checkuser == 0:
                        c.send(b"Register successfully.\n")
                        username.append(data[1])
                        password.append(data[3])
                    else:
                        c.send(b"Username is already used.\n")
                else:
                    c.send(b"Usage: register <username> <email> <password>\n")
            elif data[0]=="login":
                if len(data)==3:
                    if Login[i]==1:
                        c.send(b"Please logout first.\n")
                    else:
                        checkuser_login = 0
                        for i in range(len(username)):
                            if data[1] == username[i]:
                                checkuser_login =1
                                if data[2]==password[i]:
                                    send=data[1].encode()
                                    c.send(b"Welcome,")
                                    c.send(send)
                                    c.send(b".\n")
                                    Login[i] = 1
                                else:
                                    c.send(b"Login failed.\n")
                        if checkuser_login==0:
                            c.send(b"Login failed.\n")
                else:
                    c.send(b"Usage: login <username> <password>\n") 
            elif data[0]=="logout" and len(data)==1:
                if Login[i] ==1:
                    c.send(b"Bye,")
                    c.send(send)
                    c.send(b".\n")
                    Login[i] = 0
                else:
                    c.send(b"Please login first.\n")
            elif data[0]=="whoami" and len(data)==1:
                if Login[i] ==1:
                    c.send(send)
                    c.send(b".\n")
                else:
                    c.send(b"Please login first.\n")
            else:
                c.send(b"Usage: register <username> <email> <password>\n")
                c.send(b"Usage: login <username> <password>\n")
                c.send(b"Usage: logout\n")
                c.send(b"Usage: whoami\n")
                c.send(b"Usage: exit\n")

            c.send(b"% ")    
        except:
            pass  # 不理會錯誤
 
    