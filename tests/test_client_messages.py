from socks5mitm.protocol import client_greeting, client_connection


def test_client_greeting():
    assert client_greeting(b'\x05\x01\x00') == [0]
    assert client_greeting(b'\x05\x02\x00\x03') == [0, 3]
    assert client_greeting(b'\x05\x02\x01\x03') == [1, 3]


def test_client_connection():
    assert client_connection(
        b'\x05\x01\x00\x01\xc0\xa8\x00\x01\x00\x50'
    ).pair == ('192.168.0.1', 80)
