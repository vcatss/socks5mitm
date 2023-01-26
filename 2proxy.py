import anyio

from tiny_proxy import Socks5ProxyHandler


async def main():
    handler = Socks5ProxyHandler()
    listener = await anyio.create_tcp_listener(local_host='127.0.0.1', local_port=1080)
    await listener.serve(handler.handle)

if __name__ == '__main__':
    anyio.run(main)