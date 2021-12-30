"""
This module contains functions for auth methods.
"""


def client_auth(data):
    """
    Converts client's data to ('user', 'password')
    """
    assert data[0] == 1
    ulen = data[1]
    plen = data[2 + ulen]
    assert len(data) == ulen + plen + 3
    user = data[2 : ulen + 2].decode("utf-8")
    password = data[3 + ulen : 3 + ulen + plen].decode("utf-8")
    return (user, password)


def server_auth(status):
    """
    Server's response for client_auth
    """
    return b"\x01" + status.to_bytes(1, "big")
