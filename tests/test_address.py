from socks5mitm.protocol import Address


def test_ipv4():
    assert Address(b'\x01\x01\x02\x03\x04\x00\x50').pair == ('1.2.3.4', 80)


def test_domain():
    assert Address(b'\x03\x0agithub.com\x00\x50').pair == ('github.com', 80)


def test_ipv6():
    assert Address(
        b'\x04\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x23\x45\x67\x89\xab' +
        b'\xcd\xef\x00\x50'
    ).pair == ('0123:4567:89ab:cdef:0123:4567:89ab:cdef', 80)
