from websocket_server import WebSocketHandler


def test_websocket_handler_query_parse():
    case1 = WebSocketHandler.parse_query("GET /?a=hello HTTP/1.1")
    case2 = WebSocketHandler.parse_query("GET / HTTP/1.1")
    case3 = WebSocketHandler.parse_query("GET /?a=hello&b=world HTTP/1.1")
    case4 = WebSocketHandler.parse_query("GET /?a=hello&a=world HTTP/1.1")
    assert case1 == {'a': ['hello']}
    assert case2 == {}
    assert case3 == {'a': ['hello'], 'b': ['world']}
    assert case4 == {'a': ['hello', 'world']}
