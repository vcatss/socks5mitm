'''
This module contains SOCKS5 handler and TCP server
'''

import socketserver
import socket
import select


def exchange_loop(client, remote, handler):
    '''
    Sends client's data to remote and remote's to client.
    '''
    while True:
        ready, _, _ = select.select([client, remote], [], [])
        if client in ready:
            data = client.recv(4096)
            handler.handle_send(data)
            if remote.send(data) <= 0:
                break
        if remote in ready:
            data = remote.recv(4096)
            handler.handle_recive(data)
            if client.send(data) <= 0:
                break


def create_socket(host, port):
    '''
    Creates socket for target (remote) server.
    '''
    skt = socket.socket()
    skt.connect((host, port))
    return skt


class SOCKS5handler:
    '''
    This class handles client's requests.
    '''
    def __init__(self, request):
        self.request = request

    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        exchange_loop(self.request, create_socket(*address), self)

    def handle_handshake(self):
        return

    def handle_address(self):
        return ('1.1.1.1', 3333)

    def handle_send(self):
        return

    def handle_recive(self):
        return


class TCPhandler(socketserver.BaseRequestHandler):
    '''
    TCP handler, that uses your SOCKS5 handler.
    '''
    def __init__(self, handler):
        self.handler = handler

    def handle(self):
        self.handler(self.request).handle()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Multithreaded (async) TCP server.
    Modern browsers are making requests to the server async,
    so we need it even for only one client
    '''
    allow_reuse_address = True


def start_server(handler=SOCKS5handler, host='0.0.0.0', port=4444):
    '''
    Starts SOCKS5 server.
    '''
    ThreadedTCPServer((host, port), TCPhandler(handler))
