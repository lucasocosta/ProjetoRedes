#Socket client example in python

import socket   #for sockets
import sys  #for exit

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

host = 'google.com';
port = 80;

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

#Connect to remote server
s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

texto=raw_input("url: ")
#Send some data to remote server
message = "GET /"+texto+" HTTP/1.1\r\n\r\n"
print(message)
try :
    #Set the whole string
    s.sendall(message)
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
binary = open(texto, "wb")
binary.write(r[1])
binary.write(resto)
binary.close()
