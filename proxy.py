from time import sleep
from socks5mitm.server import SOCKS5handler, start_server
import tmproxy.tmproxy as tmproxy
import minproxy.proxy as minproxy

import json
import requests
import subprocess
import threading
from threading import Event, Thread

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

ip = None

stop_flag = threading.Event()

class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        skt = proxy.socks5((socks5_ip, socks5_port), address)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)


def getNewTMIP():
        url = "https://tmproxy.com/api/proxy/get-new-proxy"
        headers = {"Content-Type": "application/json"}
        data = {"api_key": "da1e019fd5b8265e4177a85f29645d20", "id_location": 1}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())
        if (int(response.json()['code']) == 5) == True:
            print("Get new IP fail")
            print(f"Wait for {response.json()['data']['next_request']+1}")
            sleep(response.json()['data']['next_request']+1)
            getNewTMIP()
        else:
            print("Get new IP success")
            print(response.json()['data']['socks5'])
            global ip
            ip = response.json()['data']['socks5']
            return response.json()['data']['socks5']

def execute_command():
    global ip
    print(f"Starting proxy... {ip}")
    # if(ip == None): 
    #     print("IP is None")
    #     return
    # process = subprocess.Popen(["proxy", "socks", "-t", "tcp", "-p", "0.0.0.0:4444", "-P", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # while not stop_flag.is_set():
    #     output = process.stdout.readline()
    #     if output == '' and process.poll() is not None:
    #         break
    #     if output:
    #         print(output.strip())
    

def read_output(ip):
    print(f"Starting read_output... {ip}")
    stop_flag.set()
    thread = threading.Thread(target=execute_command)
    thread.start()

from threading import Timer
class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")


# Example Usage
#read_output(getNewTMIP())

def test():
    print('a')
    read_output(getNewTMIP())

t = InfiniteTimer(5, test)
t.start()

# threading.Timer(130.0, read_output(getNewTMIP())).start()

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

