from websocket_server import WebsocketServer


PORT=9001
server = WebsocketServer(port = PORT)


# Called for every client connecting (after handshake)
@server.on_new_client()
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
@server.on_client_left()
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
@server.on_message_received()
def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))


server.run_forever()
