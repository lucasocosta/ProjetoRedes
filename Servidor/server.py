import socket
import sys
import glob, os
from thread import *

os.chdir("content/")
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8882 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        Lista=data.split()
        print(Lista)
        if "GET" in Lista:
            arq=str(Lista[1])

            if(arq=='/'):
                for file in glob.glob("*.*"):
                    reply = file +'\n'+reply
            else:
                arq=arq[1:]
                for file in glob.glob("*.*"):
                    if(file==arq):
                        binary = open(file, "rb")
                        reply = '200 ' + file+' '
                        reply = reply + binary.read()
                        break
                if '200' not in reply:
                    reply = '404'
        if not data:
            break
        conn.sendall(reply)
    Lista=[]
    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
