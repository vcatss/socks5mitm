from time import sleep
from socks5mitm.server import SOCKS5handler, start_server
import tmproxy.tmproxy as tmproxy
import minproxy.proxy as minproxy

import re
import json
import requests
import subprocess
import threading
from threading import Event, Thread

from socks5mitm.server import exchange_loop, create_socket
from socks5mitm import protocol, proxy


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


import argparse, sys
parser=argparse.ArgumentParser()

parser.add_argument("--port", help="Port of proxy")
parser.add_argument("--allowip", help="Allow ip")
# parser.add_argument("--socks5", help="Import socks5 proxy")

args=parser.parse_args()

allowip = args.allowip.split(',')
port = int(args.port) if args.port != None else 4444
# socks5 = args.socks5 

# socks5_ip = socks5.split(':')[0]
# socks5_port = int(socks5.split(':')[1])

ip = None
client_ip = None
process = None
process2 = None
checked = True

stop_flag = threading.Event()
stop_flag2 = threading.Event()

class Handle(SOCKS5handler):
    def handle(self):
        global checked
        global client_ip
        self.handle_handshake()
        address = self.handle_address()
        skt = proxy.socks5(("127.0.0.1", port+1), address)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        global checked
        global client_ip
        checked = None
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)
            

def getNewTMIP():
    global ip
    url = "https://tmproxy.com/api/proxy/get-new-proxy"
    headers = {"Content-Type": "application/json"}
    data = {"api_key": "1e20d3b694bf347fc64190d7367cc829", "id_location": 1}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    if (int(response.json()['code']) == 5) == True:
        #print("Get new IP fail")
        #print(f"Wait for {response.json()['data']['next_request']+1}")
        sleep(response.json()['data']['next_request']+1)
        return getNewTMIP()
    else:
        print(f"{bcolors.HEADER}[*] Get new IP success {bcolors.WHITE}")
        ip = response.json()['data']['socks5']
        return response.json()['data']['socks5']


def execute_command():
    global ip
    global process
    global stop_flag
    stop_flag.clear()
    print(f"Starting proxy... {ip}")
    if(ip == None): 
        print("IP is None")
        return
    process = None
    process = subprocess.Popen(["proxy", "socks", "-t", "tcp", "-p", f"127.0.0.1:{port+1}", "-P", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while not stop_flag.is_set():
        try:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                #print(output.strip())
                pass
        except:
            print("Error")
            break

def removeUFWPort(_port):
    output = subprocess.run(["ufw", "status", "numbered"], capture_output=True, text=True)
    # Search for the rule with port 1080
    for line in output.stdout.split("\n"):
        numbers = re.findall(r'\d+', line)
        if len(numbers) > 1:
            if _port ==numbers[1]:
                print(f"Rule number: {numbers[0]} : Port number: {numbers[1]}")
                ss = subprocess.run(["ufw", "--force","delete", numbers[0],"-y"], check=True)
                print(ss)
                return
                

def addUFWPort(allowip,_port):
    command = f"sudo ufw allow from {allowip} to any port {_port}"
    subprocess.run(command.split(), check=True)
    return

def execute_command2():
    global process2
    global stop_flag2
    global checked
    global client_ip
    stop_flag2.set()
    stop_flag2.clear()

    removeUFWPort(str(port+2))
    #foreach item in allowip
    for item in allowip:
        addUFWPort(item,str(port+2))

    process2 = None
    process2 = subprocess.Popen(["proxy", "sps","-P",f"socks5://127.0.0.1:{port}","-p",f":{port+2}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while not stop_flag2.is_set():
        try:
            output = process2.stdout.readline()
            if output == '' and process2.poll() is not None:
                break
            if output:
                s = str(output.strip())
                print(s)
                if "connected" in s:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', s)
                    client_ip = match.group(1)
                    print(f"{bcolors.OKBLUE}[==>*] {client_ip} {bcolors.WHITE}")
                    if match:
                        if client_ip != "127.0.0.1" and  client_ip != "localhost" and client_ip != "0.0.0.0" and match.group(1) != allowip:
                            print(f"{bcolors.FAIL}[*] Checked Fail {bcolors.WHITE}")
                            checked = False
                        else:
                            print(f"{bcolors.OKGREEN}[*] Checked OK {bcolors.WHITE}")
                            checked = True
                        #print(f"{bcolors.OKCYAN}[*] {match.group(1)}:{match.group(2)} Connection {bcolors.WHITE}")
                # print(output.strip())
        except Exception as e:
            print("Error" + str(e) )
            break
    
import os
import signal
def read_output(ip):
    global process
    global process2
    global stop_flag
    print(f"Starting read_output... {ip}")
    stop_flag.set()

    if process != None: process.terminate()
    if process2 != None: process2.terminate()

    thread = threading.Thread(target=execute_command)
    thread.start()

    thread2 = threading.Thread(target=execute_command2)
    thread2.start()

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
    print('Timer')
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

