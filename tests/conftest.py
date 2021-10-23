import logging
from time import sleep
from threading import Thread

import pytest
import websocket # websocket-client

# Add path to source code
import sys, os
if os.getcwd().endswith('tests'):
	sys.path.insert(0, '..')
elif os.path.exists('websocket_server'):
	sys.path.insert(0, '.')
from websocket_server import WebsocketServer


class TestClient():
    def __init__(self, port, threaded=True):
        self.received_messages = []
        self.closes = []
        self.opens = []
        self.errors = []

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(f"ws://localhost:{port}/",
                                  on_open=self.on_open,
                                  on_message=self.on_message,
                                  on_error=self.on_error,
                                  on_close=self.on_close)
        if threaded:
            self.thread = Thread(target=self.ws.run_forever)
            self.thread.daemon = True
            self.thread.start()
        else:
            self.ws.run_forever()

    def on_message(self, ws, message):
        self.received_messages.append(message)
        print(f"TestClient: on_message: {message}")

    def on_error(self, ws, error):
        self.errors.append(error)
        print(f"TestClient: on_error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.closes.append((close_status_code, close_msg))
        print(f"TestClient: on_close: {close_status_code} - {close_msg}")

    def on_open(self, ws):
        self.opens.append(ws)
        print("TestClient: on_open")


class TestServer(WebsocketServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received_messages = []
        self.set_fn_message_received(self.handle_received_message)

    def handle_received_message(self, client, server, message):
        self.received_messages.append(message)


@pytest.fixture(scope='function')
def threaded_server():
    """ Returns the response of a server after"""
    server = TestServer(loglevel=logging.DEBUG)
    server.run_forever(threaded=True)
    yield server
    server.server_close()


@pytest.fixture
def session(threaded_server):
    """
    Gives a simple connection to a server
    """
    conn = websocket.create_connection("ws://{}:{}".format(*threaded_server.server_address))
    yield conn, threaded_server
    conn.close()


@pytest.fixture
def client_session(threaded_server):
    """
    Gives a TestClient instance connected to a server
    """
    client = TestClient(port=threaded_server.port)
    sleep(1)
    assert client.ws.sock and client.ws.sock.connected
    yield client, threaded_server
    client.ws.close()
