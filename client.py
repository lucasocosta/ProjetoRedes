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
print 'teste github vamo que da'

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
message = "GET /"+texto+" HTTP/1.1\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)\r\nHost: "+host+"\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\nConnection: Keep-Alive"
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
#print reply
if '200'in reply:
    resposta = reply.split(' ', 3)
    cu = resposta[3].split('\r\n\r\n', 2)
    restos=s.recv(int(cu[0])+4096)
    binary = open(texto, "wb")
    total=cu[1]+restos
    binary.write(total)
    binary.close()
    #print resposta[2]
