Simple SOCKS5 server on Python3 with "MITM" features
====================================================

This is a lazily written single file library for **Python3** that implements a basic **SOCKS5** server with some [**"MITM"**](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) features.

**ATTENTION: the library was tested only on Linux!**


Use as a simple server
----------------------

~~~
$ pip3 install click
$ ./socks5mitm.py --host [localhost, 192.168.X.X, etc.] --port 4444
~~~

By default host is **0.0.0.0**, port is **4444**.


Features
--------
### Implemented:
* **Domains** and **IPv4** support
* **Spoofing** addresses and ports
* Connecting through **other SOCKS5 proxies or TOR**
* **Multithreading**

### Not implemented:
* **IPv6** support
* **Authorization**
* **Reading traffic**
* **Response statuses**

**This is the prototype version!** Library will be soon architecturally redesigned to support all of this.


Examples
--------
### $PYTHONPATH
For the examples to work, the directory with socks5mitm.py must be in **PYTHONPATH** envvar.
~~~
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
~~~


### #1 Blocker
~~~
from socks5mitm import SOCKS5Handle, Action, start_server

# Blocked Sites List
BLOCKED = ['www.google.com', 'github.com']

class Handle(SOCKS5Handle):
    def socks5handle(self, host, port):
        if host in BLOCKED:
            # If the method returns None, the server drops the connection.
            return None
        return Action(host, port)


start_server('0.0.0.0', 4444, Handle)
~~~

**examples/blocker.py** usage:
~~~
$ ./examples/blocker.py --host 0.0.0.0 --port 4444 --hosts hosts.txt
~~~
**hosts.txt** has this format:
~~~
www.google.com
github.com
~~~


### #2 Hostnamer (address spoofing)
Gives **localhost** different hostnames.
~~~
from socks5mitm import SOCKS5Handle, Action, start_server

ADDRESSES = {('test1.com', 80): ('0.0.0.0', 8888)}

class Handle(SOCKS5Handle):
    def socks5handle(self, host, port):
        address = (host, port)
        address = ADDRESSES.get(address, address)
        host, port = address
        return Action(host, port)


start_server('0.0.0.0', 4444, Handle)
~~~

**examples/hostnamer.py** usage:
~~~
$ ./examples/hostnamer.py --host 0.0.0.0 --port 4444 --hosts hosts.txt
~~~
**hosts.txt** has this format:
~~~
test1.com:80->0.0.0.0:8888
test2.com:80->0.0.0.0:9999
~~~


### #3 TORify (Connection trough other SOCKS5 servers)
Connection to some sites trough **TOR**.
~~~
from socks5mitm import SOCKS5Handle, Action, start_server

TORIFIED = ['www.google.com', 'github.com']

class Handle(SOCKS5Handle):
    def socks5handle(self, host, port):
        if host in TORIFIED:
            # ('0.0.0.0', 9050) is default TOR SOCKS5
            # server address on localhost.
            return Action(host, port, ('0.0.0.0', 9050))
        return Action(host, port)


start_server('0.0.0.0', 4444, Handle)
~~~

**examples/torify.py** usage:
~~~
$ ./examples/torify.py --host 0.0.0.0 --port 4444 --tor-host 0.0.0.0 --tor-port 9050 --hosts hosts.txt
~~~
**host.txt** has here the same format as in **Blocker**.


### #4 Logger
Logging information about connection requests.
~~~
from socks5mitm import SOCKS5Handle, Action, start_server
from time import strftime

class Handle(SOCKS5Handle):
    def socks5handle(self, host, port):
        client = self.client_address[0]
        time = strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{time}] {client} requests {host}:{port}')
        return Action(host, port)


start_server('0.0.0.0', 4444, Handle)
~~~

**examples/logger.py** usage:
~~~
$ ./examples/logger.py --host 0.0.0.0 --port 4444 --file log.txt
~~~

---
[gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
