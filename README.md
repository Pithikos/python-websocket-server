Websockets Server
=======================

A simple WebsocketsServer in Python which doesn't need any dependencies.



Usage
=======================
You can get a feel of how to use the websocket server by running

    python server.py
    
Then you need to connect from a client. Use the client.html file to connect
by using your browser's websocket implementation.


Using on your project
=======================
In order to use the websocket server in your project, simply
copy `websocket.py` to your project and `from websocket import WebSocketsServer`.
Then use the documented API below to manage the behaviour of your server.


API
=======================

The API is simply methods and properties of a WebSocketsServer instance.

**Properties**

| Property | Description          |
|----------|----------------------|
| clients  | A list of `client`   |


**Structures**
````
client = {
	'id'      : client_id,
	'handler' : client_handler,
	'address' : (addr, port)
}
````

**Methods**

| Method                | Description                                                                         | Takes           | Gives |
|-----------------------|-------------------------------------------------------------------------------------|-----------------|-------|
| set_fn_new_client()   | Sets a callback function that will be called for every new client connecting to us  | function        | None  |
| set_fn_client_left()  | Sets a callback function that will be called for every client disconnecting from us | function        | None  |
| send_message()        | Sends a message to a specific client. The message is a simple string.               | client, message | None  |
| send_message_to_all() | Sends a message to all connected clients. The message is a simple string.           | message         | None  |

