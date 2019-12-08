"""
Hi
"""
import socket
import threading
import client

SERVER_ADDRESS = ("127.0.0.1", 4261)


class Server:
    """
    The server of thee project. Manages all the clients.
    """
    def __init__(self):
        self._client_list = []
        self._client_thread_list = []
        self._server_socket = None
        self._command_queue = []

    def add_client(self, clients):
        """
        Adds the client to the client list
        :param clients: The client
        :return: Nothing
        """
        self._client_list.append(clients)

    def manage_updates(self):
        """
        Manages the messages the server gets from the clients
        :return:
        """
        while True:
            if len(self._command_queue) > 0:
                data = self._command_queue.pop()
                data = data.decode()
                print("got the message: " + data)
                key = data[0:2]
                data = data[2:]
                if key == "01":
                    user = data[:3]
                    data = data[3:]
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
            self.add_client(c)
            c.start()
            print("Client added successfully")

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
