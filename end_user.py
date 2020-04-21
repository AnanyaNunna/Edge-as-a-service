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
    l=s.recv(1024)
    f=open("./Downloads/"+x+".txt","w")
    while (l):
        l=s.recv(1024).decode()
        f.write(l)
        print("writing the file...")
    f.close()
    y=input("YOU HAVE RECEIVED THE FILE. \n Continue for more? (y/n)")
    if y =='n':
        break
