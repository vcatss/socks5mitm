#!python3

'''
Socks5 server implementation.
'''

import socketserver
import socket
import select
import click


# Default socks5 response
STUB = b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00'


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Multithreaded (async) TCP server.
    Modern browsers are making requests to the server async,
    so we need it even for only one client
    '''
    allow_reuse_address = True


# TODO: make authorization
class SOCKS5Handle(socketserver.BaseRequestHandler):
    '''
    SOCKS5 protocol request handler for TCP server.
    '''
    def socks5handle(self, host, port):  # pylint: disable=no-self-use
        '''
        It's the most important method.
        This method returns host and port.
        If output is None our proxy closes connection.
        '''
        return Action(host, port)

    def handle(self):
        try:
            self.request.recv(32)
            self.request.sendall(b'\x05\x00')
            data = self.request.recv(1024)
            self.request.send(STUB)
            host, port = read_request(data)
            out = self.socks5handle(host, port)
        except BrokenPipeError:
            return
        if out is None:
            return
        try:
            skt = out.remote_socket()
            exchange_loop(self.request, skt)
            skt.close()
        except socket.error:
            ...


class Action:
    '''
    Output of socks5handle
    '''
    def remote_socket(self):
        '''
        Creates socket for remote host
        Inits socks5 connection if needed
        '''
        host, port = self.host, self.port
        if self.proxy:
            host, port = self.proxy
        skt = socket.socket()
        skt.connect((host, port))
        if self.proxy:
            skt.send(b'\x05\x01\x00')
            if skt.recv(64) != b'\x05\x00':
                raise Exception('Proxy server refused connection')
            skt.send(write_request(self.host, self.port))
            skt.recv(64)
        return skt

    def __init__(self, host, port, proxy=None):
        self.host = host
        self.port = port
        self.proxy = proxy


def start_server(host, port, handle=SOCKS5Handle):
    '''
    Just starts server
    '''
    ThreadedTCPServer((host, port), handle).serve_forever()


# Based on https://rushter.com/blog/python-socks-server/
def exchange_loop(client, remote):
    '''
    Sends client's data to remote and remote's to client
    '''
    while True:
        ready, _, _ = select.select([client, remote], [], [])
        if client in ready:
            data = client.recv(4096)
            if remote.send(data) <= 0:
                break
        if remote in ready:
            data = remote.recv(4096)
            if client.send(data) <= 0:
                break


def read_request(data):
    '''
    Decodes request data
    Returns address and port
    '''
    host = data[3:-2]
    port = int.from_bytes(data[-2:], 'big')
    if host[0] == 3:
        host = host[2:].decode('utf-8')
    elif host[0] == 1:
        host = '.'.join([str(i) for i in host[1:]])
    elif host[0] == 4:
        # TODO: Add IPv6 support
        raise Exception('IPv6 not supported')
    return host, port


# It converts any address to domain format, so it probably won't work with IP.
def write_request(host, port):
    '''
    This function makes request data for connecting trought another proxy.
    '''
    output = b'\x05\x01\x00\x03'
    output += chr(len(host)).encode()
    output += host.encode()
    output += port.to_bytes(2, 'big')
    return output


__all__ = ['start_server', 'SOCKS5Handle', 'Action']


# It's example server on click.
@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=4444)
def main(host, port):
    '''
    Simple SOCKS5 server.
    '''
    print(f'Starting server {host}:{port}...')
    start_server(host, port)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
