import socket
import threading
import logging
import time

SERVER_ADDRESS = ('0.0.0.0', 4261)


class Server:
    def __init__(self):
        self._client_list = []
        self._client_thread_list = []
        self._server_socket = None

    def add_socket(self, client):
        self._client_list.append(client)

    def remove_socket(self, client):
        self._client_list.remove(client)

    def get_clients(self):
        try:
            while True:
                (client_socket, client_address) = self._server_socket.accept()
                self.add_socket(client_socket)
                print("Client added successfully")
                self.get_message()
        except:
            print("A problem occurred while trying to get clients")

    def get_message(self):

        while True:
            text = self._server_socket.recv(1024)
            print("got a message ")
            print(text)

    def send_message(self, message):
        pass

    def start(self):
        self._server_socket = socket.socket()
        self._server_socket.bind(SERVER_ADDRESS)
        self._server_socket.listen(1)
        print("Server is on!")
        get_clients_thread = threading.Thread(target=self.get_clients)
        get_clients_thread.start()
        """
        get_messages_thread = threading.Thread(target=self.get_message())
        get_messages_thread.start()
        """



a = Server()
a.start()
