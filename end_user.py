import sys
import os
import socket
PORT=52526
ip="192.168.0.7" # closes edge server IP that is hard coded
while True:
    x=input("Hi!  WHAT FILE WOULD YOU LIKE TO ACCESS?")
    print(x)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,PORT))
    print("Going to send request")
    s.send((x+".txt").encode())
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
    y=input("YOU HAVE RECEIVED THE FILE. \n Continue for more? (y/n)")
    if y =='n':
        break
