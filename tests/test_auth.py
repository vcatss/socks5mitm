from socks5mitm.auth import client_auth


def test_client_auth():
    assert client_auth(b'\x01\x04user\x0512345') == ('user', '12345')
