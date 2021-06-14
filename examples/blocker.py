#!python3
'''
Example Blocker SOCKS5 server.
'''

import click
from socks5mitm import SOCKS5Handle, Action, start_server

BLOCKED = []


class Handle(SOCKS5Handle):
    '''
    Blocker SOCKS5 connection handler.
    '''
    def socks5handle(self, host, port):
        if host in BLOCKED:
            return None
        return Action(host, port)


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=4444)
@click.option('--hosts')
def main(host, port, hosts):
    '''
    Click main funciton.
    '''
    global BLOCKED
    BLOCKED = open(hosts).read().split('\n')
    start_server(host, port, Handle)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
