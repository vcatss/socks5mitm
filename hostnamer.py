import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444

RULES = {"mytest1.com": "127.0.0.1"}


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        host, port = address
        address = (RULES.get(host, host), port)
        exchange_loop(self.request, create_socket(*address), self)


print(f"Starting 127.0.0.1:{PORT}...")
start_server(Handle, port=PORT)
