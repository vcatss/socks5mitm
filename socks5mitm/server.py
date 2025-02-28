import socketserver
import socks5mitm.protocol as protocol
import socket
import select
import requests


from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[0m'


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
        raddr = request
        import re
        raddr_match = re.search(r"raddr=\('(.*?)', (.*?)\)", str(raddr))
        if raddr_match:
            client_ip = raddr_match.group(1)
            client_port = raddr_match.group(2)
            print(f"{bcolors.OKCYAN}[*] {client_ip}:{client_port} Connection {bcolors.WHITE}")
            self.client_ip = client_ip
            self.client_port = client_port

        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        self.ip = data['origin']
        print(f"{bcolors.OKCYAN}[*] {self.client_ip} {bcolors.WHITE}")

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
        print(f"{bcolors.WARNING}[{self.client_ip}:{self.client_port}] send >>> {round(send_bytes, 4)} {bcolors.WHITE}")

    def handle_recive(self, data):
        global recv_bytes
        recv_bytes += len(data)/1024/1024
        #recv_mbs = recv_bytes / 1024
        print(f"{bcolors.OKGREEN}[{self.client_ip}:{self.client_port}] revc <<< {round(recv_bytes, 4)} {bcolors.WHITE}")


from socketserver import ThreadingTCPServer, BaseRequestHandler
import http.client



def start_server(sockshandler=SOCKS5handler, host="0.0.0.0", port=4444):
    class TCPhandler(socketserver.BaseRequestHandler):
        handler = sockshandler

        def handle(self):
            try:
                self.handler(self.request).handle()
            except:
                ...

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    class HTTPProxyHandler(BaseRequestHandler):
        def handle(self):
            # Parse the incoming request
            request = self.request.recv(4096).decode()
            request_parts = request.split("\n")
            method, path, _ = request_parts[0].split(" ")
            headers = {}
            for line in request_parts[1:]:
                if ":" in line:
                    name, value = line.split(":", 1)
                    headers[name.strip()] = value.strip()
            # Connect to the destination server
            conn = http.client.HTTPSConnection(headers["Host"])
            conn.request(method, path, headers=headers)
            # Forward the response back to the client
            response = conn.getresponse()
            self.request.sendall(response.read())

    global _host,_port
    _host = host
    _port = port
    ThreadedTCPServer((host, port), TCPhandler).serve_forever()
   # ThreadingTCPServer(("0.0.0.0", port), HTTPProxyHandler).serve_forever()


