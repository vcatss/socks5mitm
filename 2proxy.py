import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 1080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        print("[*] Connected from %s:%d" % (addr[0], addr[1]))

        client.send(b"\x05\x00")

        data = client.recv(1024)
        if not data:
            break

        if data[0] != 0x05:
            client.close()
            continue

        client.send(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
        data = client.recv(1024)

        # Extract the destination address and port
        addrtype = data[3]
        dest_addr = None
        if addrtype == 1:
            dest_addr = socket.inet_ntoa(data[4:8])
        elif addrtype == 3:
            dest_addr = data[5:5 + data[4]]
        else:
            client.close()
            continue
        dest_port = int.from_bytes(data[-2:], byteorder='big')

        # Connect to the destination server
        dest_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest_server.connect((dest_addr, dest_port))

        # Send the connection established message to the client
        client.send(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")

        # Start proxying data
        proxy_data(client, dest_server)

def proxy_data(client, dest_server):
    while True:
        data = client.recv(4096)
        if not data:
            break
        dest_server.sendall(data)

    client.close()
    dest_server.close()

if __name__ == "__main__":
    start_server()
