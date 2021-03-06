#Socket client example in python

import socket   #for sockets
import sys  #for exit
from urlparse import urlparse


#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

url = urlparse(sys.argv[1])

host = url.hostname
port = url.port
if(port==None):
    port=80
try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

#Connect to remote server
s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

texto=url.path
#Send some data to remote server
message = "GET /"+texto+" HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n\r\n"
print(message)
try :
    #Set the whole string
    s.sendall(message.encode())
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()

print 'Message send successfully'

#Now receive data
reply = s.recv(4096)

r=reply.split('\r\n\r\n', 2)
header=r[0].split()
tamanho=0
resto=''
if "Content-Length:" in header:
    i=header.index("Content-Length:")
    tamanho=header[i+1]
    if int(tamanho)>4096:
        resto=s.recv(int(tamanho))
if str(header[1]) != "200":
    texto="erro"+header[1]+".html"
print header
print r[1]
print resto
if texto =='' or texto =='/':
    texto="/index.html"
texto=texto[1:]
binary = open(texto, "wb")
binary.write(r[1])
binary.write(resto)
binary.close()
