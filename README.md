# edge-asa-service-ec2

Requirements to run the codes:
- Python 3 and above
- Required libraries in python: socket, sys, os, time, threading

Firewall inside every running system must allow TCP and ICMP traffic from all sources.
Port numbers (PORT and PORT_C ) taken up by this application must not be an assigned port for any other application.

Before running any code, check if the variables(HOST and ORIGINIP) at the Edge server and Origin server IP's are correctly configured.

### If you are a edge server  - To run edge.py

(1) Make sure you have the edgestat.txt, priority.txt and cache.txt with the right format. The ending of every line must be a line break, in order to not encounter errors.
cache.txt - contains rfc file list of the local machine
edgestat.txt - contains a list of mapping between every edgeserver IP and its rfc file contents
priority.txt - contains a list of all edge servers that must be contacted in-order , which is unique to every edge server

(2) Make sure the /files/ folder in the same directory contains the required rfc files, as mentioned in the cache.txt.

(3) Origin IP, HOST IP (local machine IP) must be specified appropriately. 

Default ports are 52525 (edge server listens at this port ) and 52526 (origin server listens at this port)
This code must be simultaneously running before any end user can use this applicaiton.
One can run this code on the CLI :

$python3 edge.py

If liscence key is asked when contacting the origin server, it is set to(in our implementation): 987654321

### If you are a origin server

(1) Make sure you have the /files/ directory filled with all the content that you are making available to the end users. 

(2) Also there must be an auth.txt which contains a list of authorised edge server IPs.

This code must be simulateoulsy running if the end user requests for a file, that none of the edge users have.
One can run this code by:

$python3 origin.py

### If you are an end user

(1) Make sure that the HOST IP is appropriately hard coded to the IP of the edge server closest to it. 
(2) Make sure that there is a /Downloads file in the same directory where the requested RFC files will be stored.

The end user can run this code by:

$python3 end_user.py

File requests must be given only in the following format: rfcxxx (where xxx is the rfc file number)
Only files are that available in the Origin server can be requested.

