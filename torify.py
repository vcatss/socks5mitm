import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket
from socks5mitm import protocol, proxy


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        skt = proxy.socks5(("116.96.17.21", 33513), address)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)


print(f"Starting 127.0.0.1:{PORT}...")
start_server(Handle, port=PORT)
