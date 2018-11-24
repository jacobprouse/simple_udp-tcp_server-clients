import sys
import time
import socket
import datetime
import numpy as np
import matplotlib.pyplot as plt

#create udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

#store host and port variables
host = 'localhost'
port = 12000

#count for sequence number
num_pings = 1

#count for # of packet losses
packetlosses = 0

#creation of array for RTTs
rtt_array = [0]

#loop until all pings are sent
while(num_pings <= 200):
    
    #message by normal format
    msg = 'Ping ' + str(num_pings) + ' ' + str(datetime.datetime.now())
    
    #time when sent
    send_time_ms = time.time()
    
    #send to server
    s.sendto(msg.encode('utf-8'), (host, port))
    
    #increment pings
    num_pings += 1
    
    #if reply is greater than 2 seconds, timeout
    s.settimeout(2)
    
    try:
        #recieve server reply
        message, address = s.recvfrom(1024)
        
        #time recieved
        recv_time_ms = time.time()
    
        #print reply
        print('Server reply: ' + message.decode('utf-8'))
        
        #getting individual packet RTTs and mulitply by 1000 to get ms
        rtt_time_ms = round(recv_time_ms - send_time_ms,3)*1000

        #adding packet RTTs to array
        rtt_array.append(rtt_time_ms)
        
    except socket.timeout:
        print('Request timed out')
        #record lost packets
        packetlosses = packetlosses + 1
        continue

#prints rate of packet losses in %
print('Packet loss rate: ' + str(round((packetlosses/num_pings)*100,1)) + '%')

#delete inital 0 entry of array 
del rtt_array[0]

#prints min, max, and std
minimum = np.amin(rtt_array)
maximum = np.amax(rtt_array)
std = round(np.std(rtt_array), 3)
average = round(np.mean(rtt_array, dtype=np.float64), 3)

print('Min RTT(ms): ' + str(minimum) + ' || Max RTT(ms): ' + str(maximum) + ' || Average RTT(ms): ' + str(average) + ' || Standard Deviation: ' + str(std))

#get numpy array
a = np.array(rtt_array)

#generate histogram from numpy array
n, bins, patches = plt.hist(x=a, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)

#set axis and grid lines
plt.grid(axis='y', alpha=0.75)

#label axis
plt.xlabel('Time(ms)')
plt.ylabel('Pings')

#title graph
plt.title('Ping Times')

#show graph
plt.show()






    
    
    