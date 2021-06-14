#!python3
'''
Example Torify SOCKS5 server.
'''

import click
from socks5mitm import SOCKS5Handle, Action, start_server

TORIFIED = []
TOR_HOST = '0.0.0.0'
TOR_PORT = 9050


class Handle(SOCKS5Handle):
    '''
    Torify SOCKS5 connection handler.
    '''
    def socks5handle(self, host, port):
        if host in TORIFIED:
            return Action(host, port, (TOR_HOST, TOR_PORT))
        return Action(host, port)


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=4444)
@click.option('--tor-host', default='0.0.0.0')
@click.option('--tor-port', default=9050)
@click.option('--hosts')
def main(host, port, tor_host, tor_port, hosts):
    '''
    Click main function.
    '''
    global TORIFIED, TOR_HOST, TOR_PORT
    TOR_HOST = tor_host
    TOR_PORT = tor_port
    TORIFIED = open(hosts).read().split('\n')
    start_server(host, port, Handle)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
