import socket

import socket
import threading
import logging
import time


SERVER_ADDRESS = ("127.0.0.1", 4261)


class Client(object):
    def __init__(self, sockett, address):
        self._message_list = []
        self._socket = sockett
        self._address = address
        self._updated = False

    def check_for_updates(self):
        while True:
            if len(self._message_list) > 0:
                self._updated = True
            else:
                self._updated = False

    def get_messages(self):
        return self._message_list

    def get_update(self):
        return self._updated

    def send_message(self, text):
        self._socket.send(text)

    def recive_message(self):
        while True:
            data = self._socket.recv(1024)
            self._message_list.append(data)

    def start(self):
        listen_to_server_thread\
            = threading.Thread(target=self.recive_message)
        listen_to_server_thread.start()
        check_for_updates_thread\
            = threading.Thread(target=self.check_for_updates)
        check_for_updates_thread.start()


def main():
    s1 = socket.socket()
    a = Client(s1, SERVER_ADDRESS)
    a.start()


if __name__ == '__main__':
    main()
