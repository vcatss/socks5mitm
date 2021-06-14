#!python3
'''
Example Hostnamer SOCKS5 server.
'''

import click
from socks5mitm import SOCKS5Handle, Action, start_server

ADDRESSES = {}

class Handle(SOCKS5Handle):
    '''
    Hostnamer SOCKS5 connection handler.
    '''
    def socks5handle(self, host, port):
        address = (host, port)
        address = ADDRESSES.get(address, address)
        host, port = address
        return Action(host, port)


def read_address(string):
    '''
    Converts 'host:port' to ('host': port)
    '''
    string = string.split(':')
    return (string[0], int(string[1]))


def read_pair(string):
    '''
    Converts 'host1:port1->host2:port2' to
    [('host1': port1), ('host2': port2)]
    '''
    return [read_address(i) for i in string.split('->')]


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=4444)
@click.option('--hosts')
def main(host, port, hosts):
    '''
    Click main funciton.
    '''
    global ADDRESSES
    config = open(hosts).read().split('\n')
    config = [i for i in config if i]
    config = [read_pair(i) for i in config]
    ADDRESSES = {i[0]: i[1] for i in config}
    print(ADDRESSES)
    start_server(host, port, Handle)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
