import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.protocol import client_greeting, server_choise
from socks5mitm.auth import client_auth, server_auth


PORT = sys.argv[1] if len(sys.argv) > 1 else 4444


class Handle(SOCKS5handler):
    def handle_handshake(self):
        methods = client_greeting(self.request.recv(1024))
        chs = 2 if 2 in methods else 255
        self.request.send(server_choise(chs))
        data = self.request.recv(1024)
        status = 0 if client_auth(data) == ('user', '12345') else 1
        self.request.send(server_auth(status))


print(f'Starting 127.0.0.1:{PORT}...')
start_server(Handle, port=PORT)
