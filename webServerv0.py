#import socket module
from socket import *  # @UnusedWildImport
import sys # In order to terminate the program @Reimport
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept()
    
    print('Connected to client')
    
    try:
        #recieve message from client
        message = connectionSocket.recv(1024)
        
        #decode the string from bytes to string
        string = message.decode('utf-8')
        
        #split string, 1st place element will be name of html
        filename = string.split()[1]

        #open file with file handler
        f = open(filename[1:])
        
        outputdata = f.read()
        
        #Send one HTTP header line into socket
        h = 'HTTP/1.1 200 OK\r\n'
        
        connectionSocket.send(h.encode('utf-8'))
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        h = 'HTTP/1.1 404 Not Found\n'
        
        connectionSocket.send(h.encode('utf-8'))

        #Close client socket
        connectionSocket.close()

serverSocket.close()

sys.exit()#Terminate the program after sending the corresponding data