# -*- coding: utf-8 -*-
import socket


def zclient(host, port, content):
    """

    Args:
        host:
        port:
        content:

    Returns:

    """
    # 这里这所以没有用with关键字, 是因为在HTTPServer时， socket无法进入，q
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('send all', content)
    s.sendall(content)
    data = s.recv(65537)
    print(data)
    s.close()


if __name__ == '__main__':
    print('client start\t....')
    zclient('localhost', 8000, b'hello')
    print('client end\t....')
