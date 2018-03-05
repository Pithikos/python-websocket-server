from time import sleep
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


def test_text_message_of_length_1(session):
    client, server = session
    server.send_message_to_all('$')
    assert client.recv() == '$'


def test_text_message_of_length_125B(session):
    client, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqr125'
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_126B(session):
    client, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrs126'
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_127B(session):
    client, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrst127'
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_208B(session):
    client, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw208'
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_1251B(session):
    client, server = session
    msg = ('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqr125'*10)+'1'
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_68KB(session):
    client, server = session
    msg = '$'+('a'*67993)+'68000'+'^'
    assert len(msg) == 68000
    server.send_message_to_all(msg)
    assert client.recv() == msg


def test_text_message_of_length_1500KB(session):
    """ An enormous message (well beyond 65K) """
    client, server = session
    msg = '$'+('a'*1499991)+'1500000'+'^'
    assert len(msg) == 1500000
    server.send_message_to_all(msg)
    assert client.recv() == msg
