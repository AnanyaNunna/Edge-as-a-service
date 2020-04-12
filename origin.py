import os
import sys
import threading
import time

#create a socket and listen
#check auth.txt
#If in auth.txt -> process file request
# ELSE register and add the auth.txt -> process file request

HOST = 0.0.0.1
PORT = 4567

class Threads:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
    
    def service(self):
        self.s.listen()
        print("Listening at port:" + str(PORT))
        while True:
            conn, addr = self.s.accept()
            # collecting the time stamp immediately after the connection has been accepted
            time_stamp = datetime.now()
            hostIP_port = str(addr[0])
            f = open("auth.txt",'r'):
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
                    conn.send("Hey! Don't check for the file it's not there!")
            else:
                conn.send(b"Enter the license key, please: ")
                auth_msg = (conn.recv(1024).decode())
                if auth_msg == "987654321":
                    f = open("auth.txt",'a')
                    f.write(hostIP_port)
                    print("Welcome! You are registered")
                    #To be SFTPed directory_name="/files/"+req_msg
                    conn.send("Hey! Don't check for the file it's not there!")
                else:
                    print("False identification. Intruder alert !  CYBER CELL NOTIFIED")


proc1 = Threads()

thread1 = threading.Thread(name = "File request processing", target = proc1.service)

thread1.start()

