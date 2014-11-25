import _bootstrap_
from websocket import WebSocketsServer
from time import sleep
'''
This creates just a server that sends 4 messages on a newly
connected client: 
    
    1. A message of length less than 126
    2. A message of length 126
    3. A message of length 127
    4. A message of length bigger than 127
    5. A huge message
    
Reconnect to get the next message
'''

msg1 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqr125'                                  # 125
msg2 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrs126'                                 # 126
msg3 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrst127'                                # 127
msg4 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
       'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw208'   # 208
msg5 = (msg1*10)+'1'       # 1251
msg6 = ('a'*67995)+'68000' # 68000
msg7 = ('a'*1500000)+'1500000' # 1.5MB

counter = 0

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	global counter
	if counter == 0:
		print("Sending message 1 of length %d" % len(msg1))
		server.send_message(client, msg1)
	elif counter == 1:
		print("Sending message 2 of length %d" % len(msg2))
		server.send_message(client, msg2)
	elif counter == 2:
		print("Sending message 3 of length %d" % len(msg3))
		server.send_message(client, msg3)
	elif counter == 3:
		print("Sending message 4 of length %d" % len(msg4))
		server.send_message(client, msg4)
	elif counter == 4:
		print("Sending message 5 of length %d" % len(msg5))
		server.send_message(client, msg5)
	elif counter == 5:
		print("Sending message 6 of length %d" % len(msg6))
		server.send_message(client, msg6)
	elif counter == 6:
		print("Sending message 7 of length %d" % len(msg7))
		server.send_message(client, msg6)
	else:
		print("No errors")
	counter += 1


PORT=13254
server = WebSocketsServer(PORT)
server.set_fn_new_client(new_client)
server.run_forever()
