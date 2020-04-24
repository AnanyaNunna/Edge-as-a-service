import sys
import os
import time
import socket
PORT=52526
ip="52.14.167.243" # closes edge server IP that is hard coded
while True:
    x=input("Hi!  WHAT FILE WOULD YOU LIKE TO ACCESS?")
    print(x)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,PORT))
    print("Going to send request")
    s.send((x+".txt").encode())
    t1=time.time()
    print("Sent request")
    print("Waiting for file to be sent")
    l_len = int.from_bytes(s.recv(4), 'big')
    g = open("./Downloads/"+x+".txt",'w')
    while (l_len):
        print("writing the file now...")
        l=s.recv(min(l_len, 4096)).decode()
        l_len-=len(l)
        g.write(l)
    g.close()
    t2=time.time()
    print("Time taken : ",str(t2-t1),"s\n")
    y=input("YOU HAVE RECEIVED THE FILE. \n Continue for more? (y/n)")
    if y =='n':
        break
