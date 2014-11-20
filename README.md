Websockets Server
=======================

A simple fully working WebsocketsServer in Python (with no dependencies)


Usage
=======================
You can get a feel of how to use the websocket server by running

    python server.py
    
Then you need to connect from a client. Use the client.html file to connect
by using your browser's websocket implementation.


API
=======================

**Properties**
clients this is a a list of dictionaries of type { 'id': client_id, 'handler': client_handler }

**Methods**
set_fn_new_client(fn) sets a callback function to be called whenever a new client connects
set_fn_client_left(fn) sets a callback function to be called whenever a client disconnects
send_message(client_id, message)
send_message_to_all(message)

**(Callbacks)**
All callbacks are called with the parameters`client_id, server`. Id is the id of the client and server is the instance of the running server. The reason you might want server is in case you want to use a method of the server from outside the server.


Structures:
client = {
	'id'      : client_id,
	'handler' : client_handler_object
	'address' : (host, port)
}
