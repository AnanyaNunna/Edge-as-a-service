import sys
import time
import threading
import socket
import os
#(1)open socket
#CHECK IF USER IS EDGE or END USER - update flag
# Read message
#if msg == file name:
# check cache - if yes - send and job done
#              else call file -> dict conversion - and send IP to client.py
# after receiving file from client.py
#    if flag==end user
#           send the file to user
#           update cache.txt and edgestatfile
#           send edgestatfile
#    if flag==edge
#           send file to edge
#else if msg == edgestat
#       update edgestatfile

pr=[]
x=open("./priority.txt","r")
for i in x:
    pr.append(i[:-1])
HOST="192.168.0.7"
PORT=52526
PORT_C=52525
ORIGINIP="192.168.0.22"
class Threads:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        #self.c.bind((HOST, PORT_C))

    def get_cache(self):
        cache_list = []
        f=open("./cache.txt","r")
        dat=f.readlines()
        for i in dat:
            cache_list.append(i[:-1])
        return cache_list

    def write_cache(self, cache_list):
        f=open("./cache.txt","w")
        for i in cache_list:
            f.write(i)
            f.write("\n")
        f.close()

    def send(self,file_to_send,conn1,flag):
        f = open("./files/"+file_to_send,'r')
        print("Sending file now ....")
        if flag==2:
            conn1.send(("Hey there, this is "+HOST).encode())
        l=f.read()
        l_len = len(l)
        conn1.send(l_len.to_bytes(4,'big'))
        conn1.send(l.encode())
        f.close()

    def convert(self):
        d={}
        f=open("./edgestat.txt","r")
        dat=f.readlines()
        for i in dat:
            line = i.split(":")
            key = line[0]
            line[1]=line[1].strip("\n")
            edge_list = line[1].split(",")
            d[key] = edge_list
        return d

    def update_edge(self, edge_stat_dict):
        f=open("./edgestat.txt","w")
        for k,v in edge_stat_dict.items():
            f.write(k+":")
            for i in v[:-1]:
                f.write(i+",")
            f.write(v[-1]+"\n")

    def client(self, ip_or_flag , file_name,port):
        edge_stat_dict = self.convert()
        if ip_or_flag == "broadcast":
            for ip in edge_stat_dict.keys():
                if(ip != HOST):
                    self.c.connect((ip,port))
                    self.c.send("edge stats incomming".encode())
                    f1=open("./edgestat.txt","r")
                    l=f1.read()
                    l_len = len(l)
                    self.c.send(l_len.to_bytes(4,'big'))
                    self.c.send(l.encode())
                    self.c.shutdown(1)

        else:
            self.c.connect((ip_or_flag,port))
            self.c.send(file_name.encode())
            #print("sent file name to origin")
            msg=self.c.recv(1024).decode()
            print(msg)
            if "license" in msg:
                pwd=input("Authentication required: Please enter the license key:")
                self.c.send(pwd.encode())
            l_len = int.from_bytes(self.c.recv(4), 'big')
            g = open("./files/"+file_name,'w')
            while (l_len):
                print("writing the file now...")
                l=self.c.recv(min(l_len, 4096)).decode()
                l_len-=len(l)
                g.write(l)
            g.close()
            self.c.shutdown(0)
            print("Written to the file completely")
            print("file is received from origin")

    def service(self):
        while True:
            self.s.listen()
            print("Listening at port:" + str(PORT))
            conn, addr = self.s.accept()
            # collecting the time stamp immediately after the connection has been accepted
            hostIP_port = str(addr[0])
            print("Connection established: "+hostIP_port)
            edgestat_dict = self.convert()
            if hostIP_port in edgestat_dict.keys():
                flag = 1
                print("another edge server")
            else:
                flag = 2
                print("End user is sending")

            req_msg = (conn.recv(1024).decode())
            req_msg = str(req_msg)
            print(req_msg)
            if ".txt" in req_msg or flag == 2:
                cache_list = self.get_cache()
                print("entered .txt loop")
                print(cache_list)
                if req_msg.split(".")[0] in cache_list:
                    print("entered .txt loop")
                    self.send(req_msg,conn,2)
                    print("sent .txt")
                    cache_list.remove(req_msg.split(".")[0])
                    cache_list.insert(0,req_msg.split(".")[0])
                    self.write_cache(cache_list)
                    print("updated cache")

                else:
                    cache_list = self.get_cache()
                    edge_stat_dict = self.convert()
                    print(edge_stat_dict)
                    call_origin = True
                    for i in pr:
                        if req_msg.split(".")[0] in edge_stat_dict[i]:
                            print("call client with the edge IP")
                            call_origin = False
                            self.client(i,req_msg,PORT)
                            break

                    if call_origin:
                        print("Calling origin")
                        self.client(ORIGINIP,req_msg,PORT_C)
                        
                    self.send(req_msg, conn,1)
                    if len(cache_list) > 9:
                            cache_list.pop()
                    cache_list.insert(0,req_msg.split(".")[0])
                    self.write_cache(cache_list)
                    edge_stat_dict[HOST]=cache_list
                    print(edge_stat_dict)
                    self.update_edge(edge_stat_dict)
                    self.client("broadcast",req_msg,PORT)

            elif "edge" in req_msg:
                f=open("./edgestat.txt","w")
                l_len = int.from_bytes(self.s.recv(4), 'big')
                while (l_len):
                    print("writing the file now...")
                    l=self.s.recv(min(l_len, 4096)).decode()
                    l_len-=len(l)
                    f.write(l)
                f.close()
           

proc1 = Threads()

proc1.service()
