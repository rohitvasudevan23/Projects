from __future__ import division
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import random
import sys
import os

x = y = -1
i = -1
stock_folder = 'test'

def get_file_name(req_recv):
	global filelist, i
	req_list = req_recv.split(';')
	filename = ''
	if len(req_list) > 0:
		if req_list[0] == u'req':
			msg = req_list[1].split(':')
			if msg[0] == 'send':
				filename = msg[1]
	return filename

def get_prediction_file_name(req_recv):
	global filelist, i
	req_list = req_recv.split(';')
	filename = ''
	if len(req_list) > 0:
		if req_list[0] == u'req':
			msg = req_list[1].split(':')
			if msg[0] == 'result':
				filename = msg[1]
	return filename

def get_file_content(req_recv):
	global filelist, i
	req_list = req_recv.split(';')
	file_content = ''

	if len(req_list) > 0:
		if req_list[0] == u'req':
			msg = req_list[1].split(':')
			if msg[0] == 'send':
				filename = msg[1]
				with open('individual_stocks_5yr/'+filename,'rb') as csv_stock_fp:
					file_content = csv_stock_fp.read()
						
					i += 1
					if filelist[i] == msg[1]:
						i += 1
					
	return response

def process_request(req_recv):
	global filelist, i
	req_list = req_recv.split(';')
	response = ''

	if len(req_list) > 0:
		if req_list[0] == u'req':
			msg = req_list[1].split(':')
	
			if msg[0] == 'csv':
				response = str('res;csv:'+filelist[i]).encode()
				i += 1
				
	return response

filelist = os.listdir(stock_folder)
print "len(filelist): " + str(len(filelist))

HOSTNAME = ''       # blank for any address
PORTNUMBER = 11267  # number for the port
BUFFERSIZE = 1024     # size of the buffer

SERVER_ADDRESS = (HOSTNAME, PORTNUMBER)
SERVER = Socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(SERVER_ADDRESS)

SERVER.listen(1)

while i < len(filelist):
	print("waiting for connection")
	client, client_addr = SERVER.accept()
	print "client_addr: " + str(client_addr[0])
	# req;csv
	req_recv = client.recv(BUFFERSIZE).decode()
	print "req_recv: "+ req_recv
	
	print "i: " + str(i)
	
	if 'req;csv' in req_recv:
		response = process_request(req_recv)
		print "response: " + response
		client.send(response)
	elif 'req;send' in req_recv:
		filename = get_file_name(req_recv)
		print "filename: " + filename
		filename = filename.encode("ascii")
		with open(stock_folder + '/'+ filename, 'rb') as stock_csv_fp:
			for line in stock_csv_fp:
				client.send(line)
	elif 'req;result' in req_recv:
		filename = get_prediction_file_name(req_recv)
		data = client.recv(BUFFERSIZE)
		while data:
			with open(filename, 'a+b') as prediction_fp:
				filename.write(data)
			data = client.recv(BUFFERSIZE)
	client.close()