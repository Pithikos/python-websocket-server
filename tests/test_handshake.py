import _bootstrap_
from websocket_server import *

class DummyWebsocketHandler(WebSocketHandler):
    def __init__(self, *_):
        pass

handler = DummyWebsocketHandler()

pairs = [
    # Key                        # Response
	('zyjFH2rQwrTtNFk5lwEMQg==', '2hnZADGmT/V1/w1GJYBtttUKASY='),
	('XJuxlsdq0QrVyKwA/D9D5A==', 'tZ5RV3pw7nP9cF+HDvTd89WJKj8=')
]

def test_hash_calculations_for_response():
	key = 'zyjFH2rQwrTtNFk5lwEMQg=='
	resp = handler.calculate_response_key(key)
	assert resp == '2hnZADGmT/V1/w1GJYBtttUKASY='

def test_response_messages():
	key = 'zyjFH2rQwrTtNFk5lwEMQg=='
	expect = \
		'HTTP/1.1 101 Switching Protocols\r\n'\
		'Upgrade: websocket\r\n'              \
		'Connection: Upgrade\r\n'             \
		'Sec-WebSocket-Accept: 2hnZADGmT/V1/w1GJYBtttUKASY=\r\n'\
		'\r\n'
	resp = handler.make_handshake_response(key)
	assert resp == expect
