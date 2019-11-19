import socket
import threading
import logging
import time


class Server:
    def __init__(self):
        self._client_list = []
        self._client_thread_list = []
        self._server_socket = None

    def add_socket(self, client):
        self._client_list.append(client)

    def remove_socket(self, client):
        self._client_list.remove(client)

    def get_client(self):
        self._server_socket.bind(('0.0.0.0', 4261))
        self._server_socket.listen(1)
        (client_socket, client_address) = self._server_socket.accept()
        self.add_socket(client_socket)

    def start(self):
        self._server_socket = socket.socket()
        get_clients_thread = threading.Thread(target=self.get_client(),
                                              args=(0,))
        get_clients_thread.start()
