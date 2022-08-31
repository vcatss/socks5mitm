"""
This module contains SOCKS5 handler and TCP server
"""

import socketserver
import socks5mitm.protocol as protocol
import socket
import select

recv_bytes = 0
send_bytes = 0

_host = ""
_port = 0

def exchange_loop(client, remote, handler):
    """
    Sends client's data to remote and remote's to client.
    """
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
    """
    Creates socket for target (remote) server.
    """
    skt = socket.socket()
    skt.connect((host, port))
    return skt


class SOCKS5handler:
    """
    This class handles client's requests.
    """

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
        global send_bytes
        send_bytes += len(data)/1024/1024
        print(f"[{_host}:{_port}] send >>> {send_bytes}")
        return

    def handle_recive(self, data):
        global recv_bytes
        recv_bytes += len(data)/1024/1024
        print(f"[{_host}:{_port}] revc <<< {recv_bytes}")
        return


def start_server(sockshandler=SOCKS5handler, host="127.0.0.1", port=4444):
    """
    Starts SOCKS5 server.
    """

    class TCPhandler(socketserver.BaseRequestHandler):
        """
        TCP handler, that uses your SOCKS5 handler.
        """

        handler = sockshandler

        def handle(self):
            try:
                self.handler(self.request).handle()
            except:
                ...

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        """
        Multithreaded (async) TCP server.
        Modern browsers are making requests to the server async,
        so we need it even for only one client
        """

        allow_reuse_address = True

    global _host,_port
    _host = host
    _port = port
    ThreadedTCPServer((host, port), TCPhandler).serve_forever()

