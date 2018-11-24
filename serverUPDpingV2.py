import time
import sys
from socket import *  # @UnusedWildImport
import re
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    
    #client's message split between spaces, format will be [Heartbeat, ###, time###]
    message_regex = re.findall(r'\w+', message.decode('utf-8'))

    #part of message with date
    sent_time_ms = float(message_regex[2]+'.'+message_regex[3])
    
    current_time_ms = time.time()
    
    time_elapsed = current_time_ms - sent_time_ms
    
    #if the time elapsed is greater than 2 seconds the packet is lost, report
    if time_elapsed >= 10:
        print('Client application has stopped')
        sys.exit()
        
    #if time_elapsed is greater than 10 seconds then the client has been shut off
    elif time_elapsed >= 2:
        msg = 'Packet '+ str(message_regex[1]) +' was lost'
        serverSocket.sendto(msg.encode('utf-8'), address)
        print('Heartbeat ' +message_regex[1]+' not recieved')
        
    else:
        print('Heartbeat '+message_regex[1]+' has been recieved')
        continue
