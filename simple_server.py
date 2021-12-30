import sys
from socks5mitm.server import start_server


port = int(sys.argv[1]) if len(sys.argv) > 1 else 4444

print(f"Starting 127.0.0.1:{port}...")

start_server(host="127.0.0.1", port=port)
