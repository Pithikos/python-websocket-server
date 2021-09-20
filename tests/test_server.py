from utils import session, server

import pytest


def test_client_closes_gracefully(session):
    client, server = session
    assert client.connected
    assert server.clients
    old_client_handler = server.clients[0]["handler"]
    client.close()
    assert not client.connected

    # Ensure server closed connection.
    # We test this by having the server trying to send
    # data to the client
    assert not server.clients
    with pytest.raises(BrokenPipeError):
        old_client_handler.connection.send(b"test")
