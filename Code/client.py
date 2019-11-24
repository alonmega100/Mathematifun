import socket

import socket
import threading
import logging
import time


SERVER_ADDRESS = ("127.0.0.1", 4261)


class Client:
    def __init__(self, _send_socket, _receive_socket):
        self._message_list = []
        self._send_socket = _send_socket
        self._receive_socket = _receive_socket

    def connect_to_server(self):
        self._send_socket.connect(SERVER_ADDRESS)
        self._receive_socket.connect(SERVER_ADDRESS)

    def send_message(self):
        text = "Phortophintesa, pizoozim"
        self._send_socket.send(text)

    def start(self):
        self.connect_to_server()


s1 = socket.socket()
s2 = socket.socket()
a = Client(s1, s2)
a.start()
