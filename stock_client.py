import random
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
import pandas as pd
import os
from fbprophet import Prophet

response = ''
i = 0

HOSTNAME = '54.175.246.149'  # on same host
PORTNUMBER = 11267      # same port number
BUFFERSIZE = 1024         # size of the buffer


SERVER_ADDRESS = (HOSTNAME, PORTNUMBER)

while 1:

	CLIENT = Socket(AF_INET, SOCK_STREAM)
	CLIENT.connect(SERVER_ADDRESS)

	if response == '':
		CLIENT.send(str('req;csv').encode())
		response = CLIENT.recv(BUFFERSIZE).decode()
	else:
		res_list = response.split(';')
		
		if len(res_list) > 0 and res_list[0] != '':
			
			msg = res_list[1].split(':')
			
			if msg[0] == u'csv':
				filename = msg[1]
				print "filename: " + filename
				CLIENT.send(str('req;send:'+filename))
				
				filedata = CLIENT.recv(BUFFERSIZE)
				
				if os.path.isfile(filename):
					os.remove(filename)

				while filedata:
					with open(filename,'a+b') as stock_csv_fp:
						stock_csv_fp.write(filedata)
					filedata = CLIENT.recv(BUFFERSIZE)	
				
				fname, file_extension = os.path.splitext(filename)

				df = pd.read_csv(filename, encoding='utf-8')
				new_df = df[['date', 'close']]
				new_df.columns = ['ds', 'y']
				m = Prophet()
				m.fit(new_df);

				future = m.make_future_dataframe(periods=365)
				forecast = m.predict(future)
				forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

				m.plot(forecast).savefig(fname+'.png');

				# CLIENT.send(str('req;result:'+fname+'.png'))
    			
    			# with open(fname+'.png','rb') as prediction_fp:
    			# 	for line in prediction_fp:
    			# 		CLIENT.send(line)
				
				response = ''

	print "response: " + response
	CLIENT.close()