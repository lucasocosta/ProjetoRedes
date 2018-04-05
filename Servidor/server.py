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
        if os.path.isdir(path+arq): #se eh diretorio
            reply= reply+get_dir(path+arq)
        else:
            arq=arq[1:] #remove o / do inicio
            if os.path.isfile(path+arq):
                reply = reply+get_ok(path+arq)
            else:
                reply = reply+get_notFound(path)
    return reply

def get_ok(arquivo):
    reply=''
    tamanho=os.path.getsize(arquivo)
    binary = open(arquivo, "rb")
    reply = reply+'200 OK'+'\r\n'
    reply=reply+'Content-Length: '+str(tamanho)+'\r\n\r\n'
    reply = reply + binary.read()+"\r\n\r\n"
    return reply
def get_dir(path):
    reply=''
    if os.path.isfile(path+"index.html"):
        reply = reply+get_ok(path+"index.html")
    else:
        reply = reply+'200 OK'+'\r\n'
        reply=reply+'Content-Length: '+str(4000)+'\r\n\r\n'
        reply = reply+mkIndexOf(path)
    return reply
def get_notFound(arquivo):
    reply=''
    reply = reply+'404 not_found'+'\r\n\r\n'
    binary = open(path+"404.html", "rb")
    tamanho=os.path.getsize(path+"404.html")
    reply=reply+'Content-Length: '+str(tamanho)+'\r\n\r\n'
    reply = reply + binary.read()+"\r\n\r\n"
    return reply

def mkIndexOf(arquivo):
    index='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
    index=index+'<html>'
    index=index+'<head>'
    index=index+'<title>Index of /html</title>'
    index=index+'</head>'
    index=index+'<body>'
    index=index+'<h1>Index of /html</h1>'
    index=index+'<ul><li><a href="../"> Parent Directory</a></li>'
    dirs = os.listdir(arquivo)
    for file in dirs:
        index=index+'<li><a href="'+file+'"> '+file+'</a></li>'
    index=index+'</ul>'
    index=index+'</body></html>'
    return index

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        print data
        reply=get(data)
        if not data:
            break
        print reply
        #input("teste")
        conn.sendall(reply)
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
