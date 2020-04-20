import sys
import time
import threading
import socket
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
    pr.append(i) 
HOST="192.168.0.7"
PORT=52526
PORT_C=52527
ORIGINIP="192.168.0.7"
class Threads:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.c.bind((HOST, PORT_C))
    
    def get_cache(self):
        cache_list = []
        f=open("./cache.txt","r")
        dat=f.readlines()
        for i in dat:
            cache_list.append(i)
        return cache_list

    def write_cache(self, cache_list):
        f=open("./cache.txt","w")
        for i in cache_list:
            f.write(i)
            f.write("\n")
        f.close()
    
    def send(self,file_to_send,conn1):
        f = open("./files/"+file_to_send,'rb')
        print("Sending file now ....")
        l = f.read(1024)
        while (l):
            conn1.sendall(l)
            l = f.read(1024)
        f.close()
        
    def convert(self):
        d={}
        f=open("./edgestat.txt","r")
        dat=f.readlines()
        for i in dat:
            line = i.split(":")
            key = line[0]
            edge_list = line[1].split(",")
            d[key] = edge_list
        return d

    def update_edge(self, edge_stat_dict):
        f=open("./edgestat.txt","w")
        for k,v in enumerate(edge_stat_dict):
            f.write(k+":")
            for i in v[:-1]:
                f.write(i+",")
            f.write(v[-1]+"\n")
    
    def client(self, ip_or_flag , file_name):
        edge_stat_dict = convert()
        if ip_or_flag == "broadcast":
            for ip in edge_stat_dict.keys():
                c.connect(ip,PORT_C)
                c.sendall("edge stats incomming")
                f1=open("./edgestat.txt","rb")
                l=f1.read(1024)
                while(l):
                    c.sendall(l)
                    l=f1.read(1024)
        
        else:
            f = open("c_"+file_name,'w')
            c.connect(ip_or_flag,PORT_C)
            c.sendall(file_name)
            while (l):
                l=c.recv(1024)
                f.write(l)
            f.close() 
            os.system("cp c_"+file+" "+file)
            os.system("rm c_"+file)
        
    def service(self):
        self.s.listen()
        print("Listening at port:" + str(PORT))
        while True:
            conn, addr = self.s.accept()
            # collecting the time stamp immediately after the connection has been accepted
            time_stamp = datetime.now()
            hostIP_port = str(addr[0])
            print("Connection established"+hostIP_port)
            if hostIP_port in convert().keys():
                flag = 1
                print("another edge server")
            else:
                flag = 2
                print("End user is sending")

        req_msg = (conn.recv(1024).decode())
        req_msg = str(req_msg)

        if ".txt" in req_msg or flag == 2:
            cache_list = get_cache()
            if req_msg.split(".")[0] in cache_list:
                send(req_msg,conn)
                cache_list.remove(req_msg.split(".")[0])
                cache_list.insert(0,req_msg.split(".")[0])
                write_cache(cache_list)
                print("updated cache")

            else:
                cache_list = get_cache()
                edge_stat_dict = convert()
                call_origin = True
                for i in pr: 
                    if req_msg.split(".")[0] in edge_stat_dict[i]:
                        print("call client with the edge IP")
                        call_origin = False
                        client(i,req_msg)
                        break

                if call_origin:
                    client(ORIGINIP,req_msg)
                    print("Calling origin")
                
                while True: #better way maybe timeout
                    if req_msg in os.listdir("./files/"):
                        send(req_msg, conn)
                        break
                if len(cache_list) > 9:
                        cache_list.pop()
                cache_list.insert(0,req_msg.split(".")[0])
                write_cache(cache_list)
                edge_stat_dict[hostIP_port]=cache_list
                update_edge_cache(edge_stat_dict)
                client("broadcast",req_msg)

        elif "edge" in req_msg:
            f=open("./edgestat.txt","w")
            while True:
                recv_edge = conn.recv(1024).decode()
                if not recv_edge:
                    break
                f.write(recv_edge)

proc1 = Threads()

proc1.service()



            


                








