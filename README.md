Websocket Server
=======================

[![CircleCI](https://circleci.com/gh/Pithikos/python-websocket-server/tree/master.svg?style=svg)](https://circleci.com/gh/Pithikos/python-websocket-server/tree/master)

A minimal Websockets Server in Python with no external dependencies.

  * Python2 and Python3 support
  * Clean simple API
  * Multiple clients
  * No dependencies

Notice that this implementation does not support the more advanced features
like SSL etc. The project is focused mainly on making it easy to run a
websocket server for prototyping, testing or for making a GUI for your application.


Installation
=======================

You can use the project in three ways.

  1. Copy/paste the *websocket_server.py* file in your project and use it directly
  2. `pip install git+https://github.com/Pithikos/python-websocket-server` (latest code)
  3. `pip install websocket-server` (might not be up-to-date)

For coding details have a look at the [*server.py*](https://github.com/Pithikos/python-websocket-server/blob/master/server.py) example and the [API](https://github.com/Pithikos/python-websocket-server#api).


Usage
=======================
You can get a feel of how to use the websocket server by running

    python server.py

Then just open `client.html` in your browser and you should be able to send and receive messages.


Testing
=======

Run all tests

    tox


API
=======================

The API is simply methods and properties of the `WebsocketServer` class.

## WebsocketServer

The WebsocketServer can be initialized with the below parameters.

*`port`* - The port clients will need to connect to.

*`host`* - By default the `127.0.0.1` is used which allows connections only from the current machine. If you wish to allow all network machines to connect, you need to pass `0.0.0.0` as hostname.

*`loglevel`* - logging level to print. By default WARNING is used. You can use `logging.DEBUG` or `logging.INFO` for more verbose output.


### Properties

| Property | Description          |
|----------|----------------------|
| clients  | A list of `client`   |


### Methods

| Method                      | Description                                                                           | Takes           | Gives |
|-----------------------------|---------------------------------------------------------------------------------------|-----------------|-------|
| `set_fn_new_client()`       | Sets a callback function that will be called for every new `client` connecting to us  | function        | None  |
| `set_fn_client_left()`      | Sets a callback function that will be called for every `client` disconnecting from us | function        | None  |
| `set_fn_message_received()` | Sets a callback function that will be called when a `client` sends a message          | function        | None  |
| `send_message()`            | Sends a `message` to a specific `client`. The message is a simple string.             | client, message | None  |
| `send_message_to_all()`     | Sends a `message` to **all** connected clients. The message is a simple string.       | message         | None  |


### Callback functions

| Set by                      | Description                                       | Parameters              |
|-----------------------------|---------------------------------------------------|-------------------------|
| `set_fn_new_client()`       | Called for every new `client` connecting to us    | client, server          |
| `set_fn_client_left()`      | Called for every `client` disconnecting from us   | client, server          |
| `set_fn_message_received()` | Called when a `client` sends a `message`          | client, server, message |


The client passed to the callback is the client that left, sent the message, etc. The server might not have any use to use. However it is passed in case you want to send messages to clients.


Example:
````py
import logging
from websocket_server import WebsocketServer

def new_client(client, server):
	server.send_message_to_all("Hey all, a new client has joined us")

server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()
````

## Client

Client is just a dictionary passed along methods.

```py
{
	'id'      : client_id,
	'handler' : client_handler,
	'address' : (addr, port)
}
```
