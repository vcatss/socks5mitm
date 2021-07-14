'''
Functions for reading and creating messages between client and SOCKS5 server.
'''


class Address():
    '''
    Contains address in binary and text format.
    '''
    def __init__(self, binary):
        self.binary = binary
        port = int.from_bytes(binary[-2:], 'big')
        type_ = binary[0]
        assert type_ in [1, 3, 4]
        addr = binary[:-2]
        if type_ == 1:
            self.__ipv4(addr)
        if type_ == 3:
            self.__domain(addr)
        if type_ == 4:
            self.__ipv6(addr)
        self.pair = (self.__text, port)

    def __ipv4(self, addr: bytes):
        assert len(addr) == 5
        self.__text = '.'.join([str(i) for i in addr[1:]])

    def __domain(self, addr: bytes):
        assert addr[1] == len(addr) - 2
        self.__text = addr[2:].decode('utf-8')

    def __ipv6(self, addr: bytes):
        assert len(addr) == 17

        def t_byte(iterator):
            num = hex(addr[iterator+1])[2:]
            return ('0' if len(num) == 1 else '') + num

        self.__text = ':'.join([t_byte(i*2)+t_byte((i*2)+1) for i in range(8)])


def client_greeting(message):
    '''
    This message contains avalible auth methods.
    '''
    assert message[0] == 5
    assert message[1] == len(message) - 2

    return list(message[2:])


def server_choise(number):
    return b'\x05' + number(1, 'big')


def client_connection(message):
    assert message[0] == 5
    assert message[1] in [1, 2, 3]
    assert message[2] == 0

    return Address(message[3:])


def server_connection(status):
    return b'\x05' + status.to_bytes(1, 'big')
