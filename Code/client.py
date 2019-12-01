import socket

import socket
import threading
import logging
import time


SERVER_ADDRESS = ("127.0.0.1", 4261)


class Client(object):
    def __init__(self, socket, address):
        self._message_list = []
        self._socket = socket
        self._address = address

    def connect_to_server(self):
        self._socket.connect(SERVER_ADDRESS)

    def send_message(self):
        text = "Phortophintesa, pizoozim"
        self._socket.send(text)

    def recive_message(self):
        try:
            data = self._socket.recv(1024)
        except:
            print("An error occurred while listening to server")

    def start(self):
        self.connect_to_server()
        listen_to_server_thread\
            = threading.Thread(target=self.recive_message())
        listen_to_server_thread.start()


def main():
    s1 = socket.socket()
    a = Client(s1, SERVER_ADDRESS)
    a.start()


if __name__ == '__main__':
    main()
