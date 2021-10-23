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


def test_text_message_with_unicode_characters(session):
    conn, server = session
    msg = '$äüö^'
    server.send_message_to_all(msg)
    assert conn.recv() == msg


def test_text_message_stress_bursts(session):
    """ Scenario: server sends multiple different message to the same conn
    at once """
    from threading import Thread
    NUM_THREADS = 100
    MESSAGE_LEN = 1000
    conn, server = session
    messages_received = []

    # Threads receing
    threads_receiving = []
    for i in range(NUM_THREADS):
        th = Thread(
            target=lambda fn: messages_received.append(fn()),
            args=(conn.recv,)
        )
        th.daemon = True
        threads_receiving.append(th)

    # Threads sending different characters each of them
    threads_sending = []
    for i in range(NUM_THREADS):
        message = chr(i)*MESSAGE_LEN
        th = Thread(
            target=server.send_message_to_all,
            args=(message,)
        )
        th.daemon = True
        threads_sending.append(th)

    # Run scenario
    for th in threads_receiving:
        th.start()
    for th in threads_sending:
        th.start()

    # Wait for all threads to finish
    print('WAITING FOR THREADS TO FINISH')
    for th in threads_receiving:
        th.join()
    for th in threads_sending:
        th.join()

    for message in messages_received:
        first_char = message[0]
        assert message.count(first_char) == len(message)

    print()
