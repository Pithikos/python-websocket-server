import _bootstrap_
from websocket_server import WebsocketServer
from time import sleep
from testsuite.messages import *

'''
This creates just a server that will send a different message to every new connection:

    1. A message of length less than 126
    2. A message of length 126
    3. A message of length 127
    4. A message of length bigger than 127
    5. A message above 1024
    6. A message above 65K
    7. An enormous message (well beyond 65K)


Reconnect to get the next message
'''


counter = 0

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	global counter
	if counter == 0:
		print("Sending message 1 of length %d" % len(msg_125B))
		server.send_message(client, msg_125B)
	elif counter == 1:
		print("Sending message 2 of length %d" % len(msg_126B))
		server.send_message(client, msg_126B)
	elif counter == 2:
		print("Sending message 3 of length %d" % len(msg_127B))
		server.send_message(client, msg_127B)
	elif counter == 3:
		print("Sending message 4 of length %d" % len(msg_208B))
		server.send_message(client, msg_208B)
	elif counter == 4:
		print("Sending message 5 of length %d" % len(msg_1251B))
		server.send_message(client, msg_1251B)
	elif counter == 5:
		print("Sending message 6 of length %d" % len(msg_68KB))
		server.send_message(client, msg_68KB)
	elif counter == 6:
		print("Sending message 7 of length %d" % len(msg_1500KB))
		server.send_message(client, msg_1500KB)
	else:
		print("No errors")
	counter += 1


PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.run_forever()
