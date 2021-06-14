#!python3
'''
Example Logger SOCKS5 server.
'''

import click
import atexit
from time import strftime
from socks5mitm import SOCKS5Handle, Action, start_server

FILE = None


class Handle(SOCKS5Handle):
    '''
    Logger SOCKS5 connection handler.
    '''
    def socks5handle(self, host, port):
        client = self.client_address[0]
        time = strftime('%Y-%m-%d %H:%M:%S')
        log(time, client, host, port)
        return Action(host, port)


def log(time, client, host, port):
    '''
    Displays log on the screen, or writes to file.
    '''
    text = f'[{time}] {client} requests {host}:{port}'
    if FILE:
        FILE.write(text + '\n')
    else:
        print(text)


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=4444)
@click.option('--file')
def main(host, port, file):
    '''
    Click main funciton.
    '''
    global FILE
    if file:
        FILE = open(file, 'a')
    start_server(host, port, Handle)


def at_exit():
    '''
    Closes FILE, when program ends.
    '''
    if FILE:
        FILE.close()


if __name__ == '__main__':
    atexit.register(at_exit)
    main()  # pylint: disable=no-value-for-parameter
