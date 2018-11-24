from socket import *  # @UnusedWildImport
import sys #for command line arguments @Reimport

#creat socket, SOCK_STREAM for a tcp connection
client_socket = socket(AF_INET, SOCK_STREAM)

#process arguments
serverDetails = str(sys.argv)

#store args in variables
host = str(sys.argv[1])
port = int(sys.argv[2])
request = str(sys.argv[3])

#connect to server that is listening
client_socket.connect((host, port))

#generate a request header
request_header = 'GET /'+request+' HTTP/1.1\r\nHost:192.168.0.20\r\n\r\n'

#sent the GET request header
client_socket.send(request_header.encode('utf-8'))

#recieve the message
message = client_socket.recv(1024)

while 1:
    #check if the message is not None
    if message:
        print(message.decode('utf-8'))
        message = client_socket.recv(1024)
    else:
        break
    
#close connection to host
client_socket.close()

#close client
sys.exit()