"""
The main
"""

__author__ = "Alon"


from kivy.app import App
from kivy.properties import (ObjectProperty,
                             ListProperty,
                             StringProperty,
                             BooleanProperty,
                             NumericProperty)
from kivy.clock import Clock, mainthread

import threading
import logging
import time
import random


import socket
import ui
import ssl


WHITEBOARD_FILENAME = "whiteboard.png"
# hostname = "main"
# context = ssl.create_default_context()
# context.check_hostname = False
# context.verify_mode = ssl.VerifyMode.CERT_NONE


class StudyTogetherApp(App):
    """
    The main class of the project
    """
    listen_to_user_thread = ObjectProperty(None)
    my_messages = ListProperty()
    room_messages = ListProperty()
    room_id = StringProperty()
    can_signup = BooleanProperty(True)
    signup_status = StringProperty(
        "Enter your username and password then press Sign Up")
    whiteboard_filename = StringProperty(WHITEBOARD_FILENAME)
    server_ip = StringProperty()
    server_port = NumericProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_whiteboard_available')
        super().__init__(**kwargs)
        self._connection_lock = threading.Lock()
        self.connection = None
        self._login_status_lock = threading.Lock()
        self._login_status = "Not logged in"
        self.messages = []
        self.messages_lock = threading.Lock()

    @property
    def login_status(self):
        """
        property for the login status
        :return:
        """
        with self._login_status_lock:
            return self._login_status

    @property
    def connection(self):
        """
        returns the connection (socket)
        :return:
        """
        with self._connection_lock:
            return self._connection

    @connection.setter
    def connection(self, value):
        with self._connection_lock:
            self._connection = value

    def on_whiteboard_available(self, *args):
        """

        :param args:
        :return:
        """
        return

    def on_stop(self):
        """
        sends a message when the client is closed, the message stops the
        threads
        :return:
        """
        try:
            self.send_message(b"11")
        except Exception as e:
            print(e)

    def signup(self, username, password):
        """
        the function that signs you up to the app
        :param username:
        :param password:
        :return:
        """
        self.connection = socket.socket()
        self.connection.connect((self.server_ip, self.server_port))
        # self.connection = context.wrap_socket(
        #     self.connection, server_hostname=hostname)
        self.send_message(f"10{username}#{password}".encode())
        threading.Thread(target=self.receive_message).start()

    def login(self, username, password, callback):
        """
        the function that logs you into the app
        :param username:
        :param password:
        :param callback:
        :return:
        """
        self.connection = socket.socket()
        self.connection.connect((self.server_ip, self.server_port))
        # self.connection = context.wrap_socket(
        #     self.connection, server_hostname=hostname)

        self.listen_to_user_thread = threading.Thread(
            target=self.receive_message)

        self.listen_to_user_thread.start()
        print("sending info")
        msg = f"04{username}#{password}#".encode()
        self.send_message(msg)
        while True:
            time.sleep(0)
            with self.messages_lock:
                if len(self.messages) > 0:
                    with self._login_status_lock:
                        self._login_status = self.messages.pop()[2:]
                        break

        Clock.schedule_once(callback)

    @mainthread
    def update_signup_status(self, status):
        """
        required for the algorithm to sign you up
        :param status:
        :return:
        """
        self.connection.close()
        self.signup_status = status.decode()
        self.can_signup = True

    def _send_raw_data(self, data):
        total_bytes_sent = 0
        while total_bytes_sent < len(data):
            bytes_sent = self.connection.send(data[total_bytes_sent:])
            if bytes_sent == 0:
                raise RuntimeError("socket connection broken")
            total_bytes_sent += bytes_sent

    def send_message(self, msg):
        """
        sends a message to the server. follows my protocol.
        :param msg:
        :return:
        """
        self._send_raw_data(str(len(msg)).encode() + b"-" + msg)

    @mainthread
    def _add_message_to_my_messages(self, msg):
        print("Added massage to my_messages:", msg)
        self.my_messages.append(msg)

    @mainthread
    def _add_message_to_room_messages(self, msg):
        self.room_messages.append(msg)

    @mainthread
    def _write_to_img(self, img_data):
        with open(self.whiteboard_filename, 'wb') as canvas_image:
            canvas_image.write(img_data)
        self.dispatch('on_whiteboard_available')

    def _receive_length(self):
        length = b""
        while True:
            byte = self.connection.recv(1)
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
            chunk = self.connection.recv(min(1024, length - bytes_count))
            if chunk == b"":
                raise RuntimeError("Socket connection broke")
            data[bytes_count:bytes_count + len(chunk)] = chunk
            bytes_count += len(chunk)
        return data

    def receive_message(self):
        """
        the function that receives messages. runs on a thread
        :return:
        """
        while True:
            time.sleep(0)
            length = self._receive_length()
            msg = self._receive_data(length)
            print("New command from socket:", msg)
            if msg.startswith(b"08"):
                self._write_to_img(msg[3:])
            elif msg.startswith(b"05"):
                self.room_id = msg[2:].decode()
            elif msg.startswith(b"03"):
                self._add_message_to_my_messages(msg[2:].decode())
            elif msg.startswith(b"07"):
                msg = msg.decode()
                msg = msg[2:]
                index_sender = msg.find("#")
                sender = msg[:index_sender]
                msg = msg[index_sender+1:]
                data = f" {sender}: {msg}"
                self._add_message_to_room_messages(data)
            elif msg.startswith(b"10"):
                self.update_signup_status(msg[2:])
                break
            elif msg.startswith(b"11"):
                self.connection.close()
                break
            else:
                with self.messages_lock:
                    self.messages.append(msg.decode())


def main():
    """
    runs the app
    :return:
    """
    StudyTogetherApp().run()


if __name__ == '__main__':
    main()
