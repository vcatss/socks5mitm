socks5mitm
==========

This library implements the **SOCKS5** protocol, the connection handler for the **SOCKS5** server.

Features
--------
* **IPv4** and **IPv6** addresses support.
* Spoofing addresses and ports.
* Authorization.
* Connection via other **SOCKS5** proxies or **TOR**.
* Reading client requests and server responses.
* Multithreading.

Examples
--------
* `http_spy.py` --- reading paths from **HTTP** (not **HTTPS**) requests.
* `torify.py` --- redirecting requests to **\*.onion** services via **TOR**.
* `hostnamer.py` --- **SOCKS5** server with custom **DNS**.
* `simple_auth.py` --- an example of authorization.
* `simple_logger.py` --- logging `host:port`.
* `simple_server.py` --- just a simple server.
