"""
Hi
"""
import socket
import threading
import client
import time
import users_database
from room import Room

SERVER_ADDRESS = ("127.0.0.1", 4261)
USER_ID = 1


class Server:
    """
    The server of thee project. Manages all the clients.
    """
    def __init__(self):
        self._rooms = {}
        self._rooms_lock = threading.Lock()
        self._client_list = []
        self._name_list = []
        self._client_thread_list = []
        self._server_socket = None
        self._command_queue = []
        self._user_id = 1

    def find_client_id_based(self, source):
        for clients in self._client_list:
            if str(clients.get_user_id()) == str(source):
                return clients

    def find_client_username_based(self, name):
        for clients in self._client_list:
            if str(clients.get_username()) == str(name):
                return clients

    def name_list_to_string(self):
        final = ""
        for names in self._name_list:
            final += str(names) + " "
        return final

    def manage_new_client(self, clients):
        """
        Adds the client to the client list
        :param clients: The client
        :return: Nothing
        """
        print("added new client")
        clients.start()
        while not clients.get_update():
            time.sleep(0)
        clients.set_user_id(self._user_id)
        self._user_id += 1
        self._client_list.append(clients)

    def manage_updates(self):
        """
        Manages the messages the server gets from the clients
        :return:
        """
        #TODO: SOURCE CAN BE FOUND IN THE FIRST PLACE OF THE TUPLE
        database = users_database.UsersDatabase("../Data/users_database.db")
        while True:
            time.sleep(0)
            if len(self._command_queue) > 0:
                client, data = self._command_queue.pop()
                if isinstance(data, str):
                    index_of_mark = data.index("#")
                else:
                    index_of_mark = data.index(b"#")
                source = data[:index_of_mark]
                data = data[index_of_mark+1:]
                key = data[:2]
                data = data[2:]
                print(f"Key: {key} Source: {source} Data: {data}")
                if key == "01":
                    user = data[:3]
                    data = data[3:]
                    self._client_list[int(user)].send_message(data.encode())
                elif key == "02":  # Name list
                    data = "02"+str(self._name_list)
                    print("the data im about to send:  " + data)
                    self.find_client_id_based(source)\
                        .send_message(data.encode())
                elif key == "03":  # Messages
                    index_of_mark = data.index("#")
                    user_destination = data[:index_of_mark]
                    data = data[index_of_mark + 1:]
                    message = "03" + client.get_username() + "#" + data
                    self.find_client_username_based(
                        user_destination).send_message(message.encode())
                elif key == "04":  # Log in
                    index_of_mark = data.index("#")
                    username = data[:index_of_mark]
                    print("this is your username:  " + username)
                    data = data[index_of_mark + 1:]
                    index_of_mark = data.index("#")
                    password = data[:index_of_mark]
                    print("this is your password:  " + password)
                    user_exists = database.get_user(username, password)
                    print("is exists: " + str(user_exists))
                    if user_exists:
                        client.send_message(b"04Logged in")
                        client.set_username(username)
                    else:
                        client.send_message(
                            b"04Username or password are incorrect")
                elif key == "05":  # Add a new room
                    room = Room()
                    room.add_user(client)
                    with self._rooms_lock:
                        self._rooms[room.room_id] = room
                    message_to_user = "05" + str(room.room_id)
                    client.send_message(message_to_user.encode())
                    client.set_room_id(room.room_id)
                elif key == "06":  # Add user to room
                    client.set_room_id(int(data))
                    with self._rooms_lock:
                        self._rooms[int(data)].add_user(client)
                elif key == "07":  # Send a message to Room
                    pass  # TODO: ^^^^^^^^^^
                elif key == b"08":
                    room_id = client.get_room_id()
                    with self._rooms_lock:
                        print("the room id is:" + str(room_id))
                        users_in_room = self._rooms[room_id].get_copy_of_users()
                        print("username: " + client.get_username())
                    for user in users_in_room:
                        if user.get_username() != client.get_username():
                            user.send_message(b'08' + data)
                            print("username: " + user.get_username())


    def check_for_updates(self):
        """
        Checks if there are any updates from the clients.
        :return: Nothing
        """
        while True:
            time.sleep(0)
            for client in self._client_list:
                time.sleep(0)
                if client.get_update():
                    data = client.get_messages()
                    command = (client, data)
                    self._command_queue.\
                        append(command)

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
            time.sleep(0)
            (client_socket, client_address) = self._server_socket.accept()
            c = (client.Client(client_socket, client_address),)

            manage_new_client = \
                threading.Thread(target=self.manage_new_client, args=c)
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
        users_database.UsersDatabase.create_database("../Data/users_database.db")
        database = users_database.UsersDatabase("../Data/users_database.db")
        #database.add_user("b", "c")
        print(database.get_user("a", "b"))
        database.close()


a = Server()
a.start()
