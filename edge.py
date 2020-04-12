import sys
import time
import threading
import socket
#(1)open socket
#CHECK IF USER IS EDGE 
# IF NOT:
#Get file name from end user
#check if in directory
#IF in directory, 
#   fetch file from cache,  
#   rearrange and sftp to user
#ELSE check edgestat file(2)
#   if in edgestat, 
#       contact edgeserver with higher priority
#       update cache
#   else contact origin server
#        update cache
#   UPDATE edgestat and sftp to all edges
#   send to user

# IF YES:
#socket for listening to other edge client requests 
#check message for request or file updated


