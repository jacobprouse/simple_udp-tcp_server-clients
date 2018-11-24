#import socket module
from socket import *  # @UnusedWildImport
import sys # In order to terminate the program @Reimport
import threading#for multithreading

#function for handling making new client threads
def handler(connSocket, addr):
    while True:
        try:
            #recieve message from client
            message = connSocket.recv(1024)
            
            if message:
                #decode the string from bytes to string
                string = message.decode('utf-8')

                #split string, 1st place element will be name of html
                filename = string.split()[1]
        
                #open file with file handler
                f = open(filename[1:])
                
                #read the html file and store in string array
                outputdata = f.read()
                
                #Send one HTTP header line into socket
                h = 'HTTP/1.1 200 OK\r\n'
                
                #encode header into bytes then sent it to client
                connSocket.send(h.encode('utf-8'))
                
                #Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    connSocket.send(outputdata[i].encode())
                
                #aknowledge end of file
                connSocket.send("\r\n".encode())
                break
                
            else:
                #if the message has nothing then the client is disconnected
                break
            
            
            
        except IOError:
            #Send response message for file not found
            h = 'HTTP/1.1 404 Not Found\n'
            connSocket.send(h.encode('utf-8'))

    print(str(addr) + ' - client disconnected')
    connSocket.close()
        
#main thread for listening on port 12000
if __name__ == '__main__':

    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a sever socket
    # Assign IP address and port number to socket
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    #set the serverSocket to listen on ip and port
    serverSocket.bind(('', 12000))
    
    #allow a que of 10 connections
    serverSocket.listen(10)
    
    while True:
        #Establish the connection
        print('Ready to serve...listening on port 12000')
        
        #accept the client connection and store their info
        connectionSocket, addr = serverSocket.accept()
        
        #show who is connected
        print('Connected from: '+ str(addr))
        
        #make a new thread with function handler, passing arguments
        threading.Thread(target=handler, args=(connectionSocket, addr)).start()
        
    serverSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

