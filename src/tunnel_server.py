# Echo server program
import socket
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port


def client(host, port, content):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(content)
        data = s.recv(1024)
        while data:
            print('client data', data)
            yield data
            data = s.recv(1024)


def server(host, port):
    logging.debug('server start...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            # content = b''
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('data', data)
                for content in client('166.111.65.135', 8000, data):
                    print('content', content)
                    conn.sendall(content)


if __name__ == '__main__':
    server(HOST, PORT)
