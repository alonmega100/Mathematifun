"""
The client object
"""

import threading
import time

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
        self._user_id = None
        self._room_id = None

    def set_room_id(self, room_id):
        """
        sets the room id for the client
        :param room_id:
        :return:
        """
        self._room_id = room_id

    def get_room_id(self):
        """
        returns the room id that the client is in right now
        :return:
        """
        return self._room_id

    def get_user_id(self):
        """
        returns the user id
        :return:
        """
        return self._user_id

    def set_user_id(self, user_id):
        """
        sets the users id
        :param user_id:
        :return:
        """
        self._user_id = user_id

    def get_username(self):
        """
        returns the username of that client
        :return:
        """
        return self._username

    def set_username(self, username):
        """
        sets the username of this client
        :param username:
        :return:
        """
        self._username = username

    def get_messages(self):
        """
        Gives the recent message
        :return: Recent message
        """
        return self._message_list.pop()

    def close_connection(self):
        """
        closes the socket
        :return:
        """
        self._socket.close()

    def get_update(self):
        """
        A check whether there is an update or no (message wise)
        :return: True or False
        """
        return len(self._message_list) > 0

    def _send_raw_data(self, data):
        total_bytes_sent = 0
        while total_bytes_sent < len(data):
            bytes_sent = self._socket.send(data[total_bytes_sent:])
            if bytes_sent == 0:
                raise RuntimeError("socket connection broken")
            total_bytes_sent += bytes_sent

    def send_message(self, msg):
        """
        sends a message to the user, follows my protocol
        :param msg:
        :return:
        """
        self._send_raw_data(str(len(msg)).encode() + b"-" + msg)

    def _receive_length(self):
        length = b""
        while True:
            byte = self._socket.recv(1)
            if byte == b"":
                raise RuntimeError("socket connection broke")
            elif byte == b"-":
                break
            length += byte
        return int(length.decode())

    def _receive_data(self, length):
        bytes_count = 0
        data = bytearray(length)
        while bytes_count < length:
            chunk = self._socket.recv(min(1024, length - bytes_count))
            if chunk == b"":
                raise RuntimeError("Socket connection broke")
            data[bytes_count:bytes_count + len(chunk)] = chunk
            bytes_count += len(chunk)
        return data

    def receive_message(self):
        """
        receives messages runs on a thread
        :return:
        """
        while True:
            time.sleep(0)
            length = self._receive_length()
            msg = self._receive_data(length)

            key = msg[:2]
            if key != b"00":
                msg = str(self._user_id).encode() + b"#" + msg
            if key != b"08":
                msg = msg.decode()
            self._message_list.append(msg)
            if key == b"10" or key == b"11":
                break

    def start(self):
        """
        Runs all the threads required
        :return: nothing
        """
        listen_to_user_thread\
            = threading.Thread(target=self.receive_message)
        listen_to_user_thread.start()
