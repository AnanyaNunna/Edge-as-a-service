import sys
import os
import socket
PORT=1111
ip=1.1.1.1 # closes edge server IP that is hard coded
while true:
    x=input("Hi!  WHAT FILE WOULD YOU LIKE TO ACCESS?")
    path=input("Where do you want it to be saved?")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ip,PORT)
    s.sendall(x+".txt")
    l=s.recv(1024)
    f=open("./Downloads/"+x+".txt","w")
    while (l):
        l=s.recv(1024)
        f.write(l)
        f.close() 
    y=input("YOU HAVE RECEIVED THE FILE. \n Continue for more? (y/n)")
    if y=='n'
        break