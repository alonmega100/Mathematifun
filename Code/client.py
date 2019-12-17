"""
Manages the receiving messages
"""
import threading
import message


SERVER_ADDRESS = ("127.0.0.1", 4261)


class Client(object):
    """
    The main code for users in the server. When the server gets a new socket
    it opens this new object for it.
    """
    def __init__(self, s, address):
        self._message_list = []
        self._socket = s
        self._address = address
        self._username = None

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_messages(self):
        """
        Gives the recent message
        :return: Recent message
        """
        return self._message_list.pop()

    def get_update(self):
        """
        A check whether there is an update or no (message wise)
        :return: True or False
        """
        return len(self._message_list) > 0

    def send_message(self, text):
        """
        Simply sends a message to the user
        :param text: The message
        :return: Nothing
        """
        self._socket.send(text.encode())

    def receive_message(self):
        """
        Receives message permanently runs on a thread
        :return:
        """
        while True:
            data = self._socket.recv(4)
            self._message_list.append(data)

    def start(self):
        """
        Runs all the threads required
        :return: nothing
        """
        listen_to_user_thread\
            = threading.Thread(target=self.receive_message)
        listen_to_user_thread.start()
