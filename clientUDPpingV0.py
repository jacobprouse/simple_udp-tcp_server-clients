import sys
import time
import socket
import datetime

#create udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 12000

num_pings = 1

while(num_pings <= 10):
    
    msg = 'Ping ' + str(num_pings) + ' ' + str(datetime.datetime.now())
    
    send_time_ms = time.time()
    
    s.sendto(msg.encode('utf-8'), (host, port))
    
    num_pings = num_pings + 1
    
    s.settimeout(2)
    
    try:
        message, address = s.recvfrom(1024)
        recv_time_ms = time.time()
    
        print('Server reply: ' + message.decode('utf-8'))
        
        #getting individual packet RTTs
        rtt_time_ms = round(recv_time_ms - send_time_ms,3)
        
        print('RTT: ' + str(rtt_time_ms))
        
    except socket.timeout:
        print('Request timed out')
        #record lost packets
        continue