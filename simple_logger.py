import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket
import pprint
from socks5mitm import protocol, proxy

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444

class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        skt = proxy.socks5(("",1000),address)
        #print(f"Request to {address[0]}:{address[1]}")
        if 1:
            skt = proxy.socks5(("127.0.0.1", 9050), address)
        else:
            skt = create_socket(*address)
        exchange_loop(self.request, skt, self)

print(f"Starting 127.0.0.1:{PORT}...")
start_server(Handle, port=PORT)
