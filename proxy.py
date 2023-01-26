from time import sleep
from socks5mitm.server import SOCKS5handler, start_server
import tmproxy.tmproxy as tmproxy
import minproxy.proxy as minproxy

import json
import requests
import subprocess
import threading


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
        ip = self.getNewTMIP()
        print("New IP: " + ip)
        self.read_output(ip)
        skt = proxy.socks5((socks5_ip, socks5_port), address)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)

    def getNewTMIP(self):
        url = "https://tmproxy.com/api/proxy/get-new-proxy"
        headers = {"Content-Type": "application/json"}
        data = {"api_key": "36c9e9ecb9677a8eb780f4d0802dc12f", "id_location": 1}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())
        print(int(response.json()['code']) == 5)
        if (int(response.json()['code']) == 5) == True:
            print("Get new IP fail")
            print(f"Wait for {response.json()['data']['next_request']+1}")
            sleep(response.json()['data']['next_request']+1)
            self.getNewTMIP()
        else:
            print("Get new IP success")
            return response.json()['data']['socks5']

    def execute_command(self,ip):
        process = subprocess.Popen(["proxy", "socks", "-t", "tcp", "-p", f"0.0.0.0:{socks5_port}", "-P", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

    def read_output(self,ip):
        thread = threading.Thread(target=self.execute_command, args=(ip,))
        thread.start()
        

print(f"Starting 127.0.0.1:{port}...")
start_server(Handle, port=port)


# It's starting a server on port 4444.
# print(f"Starting 127.0.0.1:{port}...")
# start_server(host="0.0.0.0", port=port)


# TMproxy = tmproxy.TMPRoxy("https://tmproxy.com/api/proxy", "TL9gl9QD2FqLXmWs2DReiX61TEmxsfMoiCYy74")
# TMproxy.check()

# MinProxy = minproxy.MinProxy("https://dash.minproxy.vn/api/rotating/v1/proxy","iG7J1qBTfA4TFyvTHYBOVA1HvwqCWELf")
# MinProxy.getCurrentProxy()
# MinProxy.getNewProxy()

