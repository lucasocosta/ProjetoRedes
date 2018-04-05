import socket
import sys
import glob, os
import os.path
from thread import *

path="content/"
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8880 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

def get(data):
    Lista=data.split()
    reply=''
    if "GET" in Lista:
        reply = 'HTTP/1.1 '
        arq=str(Lista[1])
        if arq.endswith('/'): #se eh diretorio
            get_dir(path+arq)
        else:
            arq=arq[1:] #remove o / do inicio
            if os.path.isfile(path+arq):
                reply = reply+get_ok(path+arq)
            else:
                reply = reply+get_notFound(path)
    return reply

def get_ok(arquivo):
    reply=''
    binary = open(arquivo, "rb")
    reply = reply+'200 OK'+'\n\n'
    reply = reply + binary.read()+"\n\n"
    return reply
def get_dir(path):
    reply=''
    if os.path.isfile(path+"index.html"):
        reply = reply+get_ok(path+arq)
    else:
        for file in glob.glob("*.*"):
            reply = file +'\n'+reply
    return reply
def get_notFound(arquivo):
    reply=''
    reply = reply+'404 not_found'+'\n\n'
    binary = open(path+"404.html", "rb")
    reply = reply + binary.read()+"\n\n"
    return reply

def mkIndexOf():
    return

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        reply=get(data)
        if not data:
            break
        print reply
        #input("teste")
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
