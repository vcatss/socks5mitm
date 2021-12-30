"""
Using this module, you can redirect traffic through other proxies.
"""

from socks5mitm.server import create_socket


def socks5(proxy, target):
    skt = create_socket(*proxy)
    skt.send(b"\x05\x01\x00")
    assert skt.recv(32) == b"\x05\x00"
    skt.send(b"\x05\x01\x00" + target.binary)
    assert skt.recv(64)[1] == 0
    return skt
