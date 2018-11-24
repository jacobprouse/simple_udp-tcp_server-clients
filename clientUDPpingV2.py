import time
import sys
import socket
import random
#create udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 12000

num_pings = 0

while True:
    num_pings += 1
    
    msg = 'Heartbeat ' + str(num_pings) + ' ' + str(time.time())
    
    rand = random.randint(0,10)
    
    #test server for detection of closing application (set to 10 seconds on server side)
    if num_pings == 10:
        time.sleep(10)
        s.sendto(msg.encode('utf-8'), (host, port))
        sys.exit()
        
    #test server for detecting lost packets (set to 2 seconds server side)
    elif rand < 3:
        time.sleep(2)
        s.sendto(msg.encode('utf-8'), (host, port))
        message, address = s.recvfrom(1024)
        print('Server reply: ' + message.decode('utf-8'))
    
    else:
        time.sleep(1)
        s.sendto(msg.encode('utf-8'), (host, port))
        
    