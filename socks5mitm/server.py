'''
This module contains SOCKS5 handler and TCP server
'''

import socketserver
import socks5mitm.protocol as protocol
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
        self.request.recv(32)
        self.request.send(protocol.server_choise(0))

    def handle_address(self):
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message).pair

    def handle_send(self, data):
        return

    def handle_recive(self, data):
        return


def start_server(sockshandler=SOCKS5handler, host='0.0.0.0', port=4444):
    '''
    Starts SOCKS5 server.
    '''
    class TCPhandler(socketserver.BaseRequestHandler):
        '''
        TCP handler, that uses your SOCKS5 handler.
        '''
        handler = sockshandler

        def handle(self):
            try:
                self.handler(self.request).handle()
            except:
                ...

    class ThreadedTCPServer(socketserver.ThreadingMixIn,
                            socketserver.TCPServer):
        '''
        Multithreaded (async) TCP server.
        Modern browsers are making requests to the server async,
        so we need it even for only one client
        '''
        allow_reuse_address = True

    ThreadedTCPServer((host, port), TCPhandler).serve_forever()
