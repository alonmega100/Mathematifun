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
    """
    def send_message(self, text):
        
        Simply sends a message to the user
        :param text: The message
        :return: Nothing
        
        self._socket.send(str(len(text)).encode())
        self._socket.send(text.encode())
    """
    def send_message(self, msg):
        length = str(len(msg))
        length_length = len(length)
        total_sent = 0
        print("length length: " + str(length_length))
        while total_sent < length_length:
            self._socket.send(length[total_sent:total_sent + 1].encode())
            total_sent += 1
            self._socket.send(b'-')
        total_sent = 0
        print(msg)
        while total_sent < int(length):
            self._socket.send(msg[total_sent:total_sent + 1].encode())
            total_sent += 1
            self._socket.send(b'-')
            self._socket.send(msg.encode())

    def receive_message(self):
        length = 0
        total_recv = 0
        msg = ""
        data = self._socket.recv(1).decode()
        while not data == "-":
            length += int(data)
            data = self._socket.recv(1).decode()
        while total_recv < length:
            data = self._socket.recv(1).decode()
            msg += data
            total_recv += 1
        self._message_list.append(msg)
        print(msg)
    """
    def receive_message(self):
        
        Receives message permanently runs on a thread
        :return:
        
        while True:
            length = self._socket.recv(1).decode()
            print("Length is " + str(length))
            data = self._socket.recv(int(length))
            self._message_list.append(data)
    """
    def start(self):
        """
        Runs all the threads required
        :return: nothing
        """
        listen_to_user_thread\
            = threading.Thread(target=self.receive_message)
        listen_to_user_thread.start()
