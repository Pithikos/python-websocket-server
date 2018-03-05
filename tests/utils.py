import logging
from threading import Thread

import pytest
from websocket import create_connection  # websocket-client

import _bootstrap_
from websocket_server import WebsocketServer


@pytest.fixture(scope='function')
def server():
    """ Returns the response of a server after"""
    s = WebsocketServer(0, loglevel=logging.DEBUG)
    server_thread = Thread(target=s.run_forever)
    server_thread.daemon = True
    server_thread.start()
    yield s
    s.server_close()


@pytest.fixture
def session(server):
    ws = create_connection("ws://{}:{}".format(*server.server_address))
    yield ws, server
    ws.close()
