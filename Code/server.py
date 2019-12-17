"""
Hi
"""
import socket
import threading
import client
import time
SERVER_ADDRESS = ("127.0.0.1", 4261)


class Server:
    """
    The server of thee project. Manages all the clients.
    """
    def __init__(self):
        self._client_list = []
        self._name_list = []
        self._client_thread_list = []
        self._server_socket = None
        self._command_queue = []

    def manage_new_client(self, clients):
        """
        Adds the client to the client list
        :param clients: The client
        :return: Nothing
        """
        clients.start()
        while not clients.get_update():
            time.sleep(0.5)
            print("w8ing")

        name = clients.get_messages()
        print(name)
        clients.set_username(name)
        print(clients.get_username())

        self._client_list.append(clients)
        print("im here")
        self._name_list.append(clients.get_username())
        print(self._name_list)

    def manage_updates(self):
        """
        Manages the messages the server gets from the clients
        :return:
        """
        while True:
            if len(self._command_queue) > 0:
                data = self._command_queue.pop()
                data = data.decode()
                key = data[0:2]
                data = data[2:]
                if key == "01":
                    user = data[:3]
                    data = data[3:]
                    self._client_list[int(user)].send_message(data)
                elif key == "02":
                    user = data[:3]
                    data = str(self._name_list)

                    self._client_list[int(user)].send_message(data)

    def check_for_updates(self):
        """
        Checks if there are any updates from the clients.
        :return: Nothing
        """
        while True:
            for clients in self._client_list:
                if clients.get_update():
                    data = clients.get_messages()
                    self._command_queue.append(data)

    def remove_client(self, clients):
        """
        Removes a client from the client list
        :param clients: the client
        :return: Nothing
        """
        self._client_list.remove(clients)

    def get_clients(self):
        """
        The function who gets new sockets permanently and saves them as
        a client. Runs on a thread.
        :return: Nothing
        """
        while True:
            (client_socket, client_address) = self._server_socket.accept()
            c = client.Client(client_socket, client_address)
            manage_new_client = \
                threading.Thread(target=self.manage_new_client(c))
            manage_new_client.start()

    def start(self):
        """
        The main function that runs the server. Manages the threads.
        :return: Nothing
        """
        self._server_socket = socket.socket()
        self._server_socket.bind(SERVER_ADDRESS)
        self._server_socket.listen(1)
        print("Server is on!")
        get_clients_thread = threading.Thread(target=self.get_clients)
        get_clients_thread.start()
        check_for_updates_thread \
            = threading.Thread(target=self.check_for_updates)
        check_for_updates_thread.start()
        manage_command_queue_thread \
            = threading.Thread(target=self.manage_updates)
        manage_command_queue_thread.start()


a = Server()
a.start()
