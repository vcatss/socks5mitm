# socks5mitm

This library implements a basic SOCKS5 server with some [MITM](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) features.

**ATTENTION: the library was tested only on Linux!**

features
--------
* IPv4 and IPv6 addresses support
* spoofing hosts and ports
* authorization
* connection via other SOCKS5
* reading messages
* multithreading

examples
--------
### 1. simple_server

~~~
from socks5mitm.server import start_server

start_server(host="127.0.0.1", port=4444)  # it's default host and port values
~~~

example usage:

~~~
$ python3 simple_server.py [PORT]
~~~

---

### 2. simple_auth

~~~
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.protocol import client_greeting, server_choise
from socks5mitm.auth import client_auth, server_auth


AUTH = ("user", "12345")


class Handle(SOCKS5handler):
    def handle_handshake(self):
        # get avalible auth methods
        methods = client_greeting(self.request.recv(1024))
        
        # choose method
        chs = 2 if 2 in methods else 255
        self.request.send(server_choise(chs))
        
        # check auth data, send bad status if it's wrong
        data = self.request.recv(1024)
        status = 0 if client_auth(data) == AUTH else 1
        self.request.send(server_auth(status))
        
        # make exception if status is't zero
        assert status == 0


start_server(Handle)
~~~

example usage:

~~~
$ python3 simple_auth.py [PORT]
~~~

---

### 3. simple_logger

~~~
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        print(f"Request to {address[0]}:{address[1]}")
        exchange_loop(self.request, create_socket(*address), self)


start_server(Handle)
~~~

example usage:

~~~
$ python3 simple_logger.py [PORT]
~~~

---

### 4. hostnamer

~~~
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket


RULES = {"mytest1.com": "127.0.0.1"}


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        host, port = address
        address = (RULES.get(host, host), port)
        exchange_loop(self.request, create_socket(*address), self)


start_server(Handle)
~~~

example usage:

~~~
$ python3 hostnamer.py [PORT]
~~~

---

### 5. torify

~~~
import sys
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket
from socks5mitm import protocol, proxy


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        if address.pair[0].split(".")[-1] == "onion":
            skt = proxy.socks5(("127.0.0.1", 9050), address)
        else:
            skt = create_socket(*address.pair)
        exchange_loop(self.request, skt, self)

    def handle_address(self):
        # return Address object (by defaut returns Address.pair)
        message = self.request.recv(1024)
        self.request.send(protocol.server_connection(0))
        return protocol.client_connection(message)


print(f"Starting 127.0.0.1:{PORT}...")
start_server(Handle, port=PORT)
~~~

example usage:

~~~
$ python3 torify.py [PORT]
~~~

---

### 6. http_spy

~~~
from socks5mitm.server import SOCKS5handler, start_server
from socks5mitm.server import exchange_loop, create_socket


class Handle(SOCKS5handler):
    def handle(self):
        self.handle_handshake()
        address = self.handle_address()
        
        # save address to use in handle_send
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


start_server(Handle)
~~~
