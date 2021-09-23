from utils import session, client_session, server
from time import sleep

import pytest


def test_send_close(client_session):
    "Ensure client stops receiving data once we send_close (socket is still open)"
    client, server = client_session
    assert client.received_messages == []

    server.send_message_to_all("test1")
    sleep(0.5)
    assert client.received_messages == ["test1"]

    # After CLOSE, client should not be receiving any messages
    server.clients[-1]["handler"].send_close()
    sleep(0.5)
    server.send_message_to_all("test2")
    sleep(0.5)
    assert client.received_messages == ["test1"]


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
