import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        self.__address = f"{address[0]}:{address[1]}"
        exchange_loop(self.request, create_socket(*address), self)

    def handle_send(self, data):
        try:
            dec = data.decode("utf-8").split(" ")
            if dec[0] not in ("GET", "POST"):
                return
            dec = dec[1]
            print(f"http://{self.__address}{dec}")
        except:
            pass


print(f"Starting 127.0.0.1:{PORT}...")
start_server(Handle, port=PORT)
