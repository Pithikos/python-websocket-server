from websocket_server import WebSocketHandler


def test_hash_calculations_for_response():
    assert WebSocketHandler.calculate_response_key('zyjFH2rQwrTtNFk5lwEMQg==') == '2hnZADGmT/V1/w1GJYBtttUKASY='


def test_response_messages():
	key = 'zyjFH2rQwrTtNFk5lwEMQg=='
	expected = \
		'HTTP/1.1 101 Switching Protocols\r\n'\
		'Upgrade: websocket\r\n'              \
		'Connection: Upgrade\r\n'             \
		'Sec-WebSocket-Accept: 2hnZADGmT/V1/w1GJYBtttUKASY=\r\n'\
		'\r\n'
	handshake_content = WebSocketHandler.make_handshake_response(key)
	assert handshake_content == expected
