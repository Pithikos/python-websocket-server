from websocket import WebSocketsServer


# Called for every client connecting (after handshake)
def new_client(client, server):
	print("Client connected (%s:%d)" % client['address'])
	server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client disconnected (%s:%d)" % client['address'])


PORT=13254
server = WebSocketsServer(PORT)

server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.run_forever()
