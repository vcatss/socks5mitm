from socks5mitm.server import SOCKS5handler, start_server
import tmproxy.tmproxy as tmproxy
import minproxy.proxy as minproxy

from socks5mitm.server import exchange_loop, create_socket
from socks5mitm import protocol, proxy

import argparse, sys
parser=argparse.ArgumentParser()

parser.add_argument("--port", help="Port of proxy")
parser.add_argument("--socks5", help="Import socks5 proxy")

args=parser.parse_args()

port = int(args.port) if args.port != None else 4444
socks5 = args.socks5 

socks5_ip = socks5.split(':')[0]
socks5_port = int(socks5.split(':')[1])

class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        #skt = proxy.socks5((socks5_ip, socks5_port), address)
        #skt = create_socket(*address)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)

print(f"Starting 127.0.0.1:{port}...")
#start_server(Handle, port=port)


# print(f"Starting 127.0.0.1:{port}...")
start_server(host="0.0.0.0", port=port)


# TMproxy = tmproxy.TMPRoxy("https://tmproxy.com/api/proxy", "TL9gl9QD2FqLXmWs2DReiX61TEmxsfMoiCYy74")
# TMproxy.check()

# MinProxy = minproxy.MinProxy("https://dash.minproxy.vn/api/rotating/v1/proxy","iG7J1qBTfA4TFyvTHYBOVA1HvwqCWELf")
# MinProxy.getCurrentProxy()
# MinProxy.getNewProxy()

