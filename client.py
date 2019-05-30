import random
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM

response = ''
i = 0

HOSTNAME = '54.175.246.149'  # on same host
PORTNUMBER = 11267      # same port number
BUFFERSIZE = 80         # size of the buffer


SERVER_ADDRESS = (HOSTNAME, PORTNUMBER)

while 1:

	CLIENT = Socket(AF_INET, SOCK_STREAM)
	CLIENT.connect(SERVER_ADDRESS)

	if response == '':
		CLIENT.send(str('req;pts').encode())
		response = CLIENT.recv(BUFFERSIZE).decode()
	else:
		res_list = response.split(';')
		
		if len(res_list) > 0 and res_list[0] != '':
			
			msg = res_list[1].split(':')
			
			if msg[0] == u'pts':
				i = msg[1]
				x_value = res_list[2].split(':')
				y_value = res_list[3].split(':')
				in_circle = 0
				if float(x_value[1])**2 + float(x_value[1])**2 <= 1:
					in_circle = 1
				
					# CLIENT = Socket(AF_INET, SOCK_STREAM)
					# CLIENT.connect(SERVER_ADDRESS)			
				CLIENT.send(str('req;result:'+str(i)+';in_circle:'+str(in_circle)).encode())
				response = CLIENT.recv(BUFFERSIZE).decode()
	print "response: " + response
	CLIENT.close()