import os
import sys
import threading
import time
import socket

#create a socket and listen
#check auth.txt
#If in auth.txt -> process file request
# ELSE register and add the auth.txt -> process file request

HOST = "192.168.149.130"
PORT = 52525

class Threads:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

    def send(self,file_to_send,conn1):
        f = open("./files/"+file_to_send,'r')
        print("Sending file now ....")
        l = f.read(1024)
        while (l):
            conn1.send(l.encode())
            l = f.read(1024)
        f.close()

    def service(self):
        self.s.listen()
        print("Listening at port:" + str(PORT))
        while True:
            conn, addr = self.s.accept()
            print("connection established with :")
            # collecting the time stamp immediately after the connection has been accepted
            time_stamp = datetime.now()
            hostIP_port = str(addr[0])
            print(hostIP_port)
            print("Connection established with !"+hostIP_port)
            f = open("auth.txt",'r')
            auth_ip_list = f.readlines()
            if hostIP_port in auth_ip_list:
                print("Oh! You are already registered")
                req_msg = (conn.recv(1024).decode())
                if 'leave'in req_msg:
                    with open("auth.txt", 'w') as f:
                        for auth_ip in auth_ip_list:
                            if hostIP_port != auth_ip.strip("\n"):
                                f.write(auth_ip)
                else:
                    #To be SFTPed directory_name="/files/"+req_msg
                    self.send(req_msg,conn)
                    print("sent the file ")
            else:
                req_msg = (conn.recv(1024).decode())
                conn.send("Enter the license key, please: ").encode()
                auth_msg = (conn.recv(1024).decode())
                if auth_msg == "987654321":
                    f = open("auth.txt",'a')
                    f.write(hostIP_port)
                    print("Welcome! You are registered")
                    self.send(req_msg,conn)
                else:
                    print("False identification. Intruder alert !  CYBER CELL NOTIFIED")


proc1 = Threads()

proc1.service()
#thread1 = threading.Thread(name = "File request processing", target = proc1.service)

#thread1.start()