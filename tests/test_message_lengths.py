def test_text_message_of_length_1(session):
    conn, server = session
    server.send_message_to_all('$')
    assert conn.recv() == '$'


def test_text_message_of_length_125B(session):
    conn, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqr125'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_126B(session):
    conn, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrs126'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_127B(session):
    conn, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrst127'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_208B(session):
    conn, server = session
    msg = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw208'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_1251B(session):
    conn, server = session
    msg = ('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
          'abcdefghijklmnopqr125'*10)+'1'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_68KB(session):
    conn, server = session
    msg = '$'+('a'*67993)+'68000'+'^'
    assert len(msg) == 68000
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_of_length_1500KB(session):
    """ An enormous message (well beyond 65K) """
    conn, server = session
    msg = '$'+('a'*1499991)+'1500000'+'^'
    assert len(msg) == 1500000
    server.send_message_to_all(msg)
    assert conn.recv() == msg
