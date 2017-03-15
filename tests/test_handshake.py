import _bootstrap_
from websocket_server import *
import pytest


class DummyWebsocketHandler(WebSocketHandler):
    def __init__(self, *_):
        pass

@pytest.fixture
def websocket_handler():
	return DummyWebsocketHandler()

def test_hash_calculations_for_response(websocket_handler):
	key = 'zyjFH2rQwrTtNFk5lwEMQg=='
	expected_key = '2hnZADGmT/V1/w1GJYBtttUKASY='
	assert websocket_handler.calculate_response_key(key) == expected_key


def test_response_messages(websocket_handler):
	key = 'zyjFH2rQwrTtNFk5lwEMQg=='
	expected = \
		'HTTP/1.1 101 Switching Protocols\r\n'\
		'Upgrade: websocket\r\n'              \
		'Connection: Upgrade\r\n'             \
		'Sec-WebSocket-Accept: 2hnZADGmT/V1/w1GJYBtttUKASY=\r\n'\
		'\r\n'
	handshake_content = websocket_handler.make_handshake_response(key)
	assert handshake_content == expected
