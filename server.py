from __future__ import division
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
import random
import sys
import os

x = y = -1
i = 1

def process_request(req_recv):
	global x, y, i
	req_list = req_recv.split(';')
	response = ''

	with open('pts.txt','r+') as pts_fp:
		pts_i = pts_fp.readline()
		pts_fp.seek(0)

		if len(req_list) > 0:
			if req_list[0] == u'req':
				msg = req_list[1].split(':')
		
				if msg[0] == 'pts':
					i = int(pts_i) + 1
					
					response = str('res;pts:'+str(i)+';x:'+str(x)+';y:'+str(y)+';').encode()
					x = y = -1
					pts_fp.truncate()
					pts_fp.write(str(i))
					pts_fp.seek(0)
				elif msg[0] == 'result':
					# parse and store in file: format - req;result:i;
					
					in_circle = req_list[2].split(':')
					
					with open('in_circle.txt','a+') as in_circle_fp:
						file_content = in_circle_fp.readline()
						
						in_circle_fp.seek(0)
						in_circle_fp.truncate()
						
						if file_content != '':
							file_content_list = file_content.split(':')
							print file_content_list
							new_in_circle_value = int(file_content_list[1])+int(in_circle[1])
							print new_in_circle_value
							in_circle_fp.write('in_circle:'+str(new_in_circle_value))
						else:
							in_circle_fp.seek(0)
							in_circle_fp.write('in_circle:'+str(in_circle[1]))
					
					i = int(pts_i) + 1
					if i == msg[1]:
						i += 1
					
					response = str('res;pts:'+str(i)+';x:'+str(x)+';y:'+str(y)+';').encode()
					x = y = -1
					pts_fp.seek(0)
					pts_fp.truncate()
					pts_fp.write(str(i))
					pts_fp.seek(0)
	return response

if len(sys.argv) == 2:
	no_of_points = int(sys.argv[1])

	if os.path.isfile("in_circle.txt"):
		os.remove("in_circle.txt")

	with open('pts.txt', 'w') as pts_fp:
		pts_fp.write('0')

	HOSTNAME = ''       # blank for any address
	PORTNUMBER = 11267  # number for the port
	BUFFERSIZE = 80     # size of the buffer

	SERVER_ADDRESS = (HOSTNAME, PORTNUMBER)
	SERVER = Socket(AF_INET, SOCK_STREAM)
	SERVER.bind(SERVER_ADDRESS)

	SERVER.listen(1)

	while i < no_of_points:
		if x < 0:
			x = random.uniform(0,1)
		
		if y < 0:
			y = random.uniform(0,1)
			
		print("waiting for connection")
		client, client_addr = SERVER.accept()
		print "client_addr: " + str(client_addr[0])
		# req;pts
		req_recv = client.recv(BUFFERSIZE).decode()
		print "req_recv: "+ req_recv
		response = process_request(req_recv)
		print "response: " + response
		client.send(response)
		client.close()

	with open('in_circle.txt', 'r') as in_circle_fp:
		in_circle_value = in_circle_fp.readline()
		in_circle_list = in_circle_value.split(':')
		
		if in_circle_list[1] != '':
			ratio = int(in_circle_list[1]) / no_of_points
			pi = ratio * 4
			print "pi: " + str(pi)
else:
	print "missing no of points"