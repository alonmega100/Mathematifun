"""
The main
"""

__author__ = "Alon"


from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.clock import Clock

import socket
import threading
import logging
import time
import random


import socket
import ui


# TODO ^^^^^^^^^^^^^

SERVER_ADDRESS = ("127.0.0.1", 4261)


class MathematifunApp(App):
    """
    The big app
    """
    listen_to_user_thread = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connection_lock = threading.Lock()
        self.connection = None
        self._login_status_lock = threading.Lock()
        self._login_status = "Not logged in"

        self.messages = []

        self.messages_lock = threading.Lock()

    @property
    def login_status(self):
        with self._login_status_lock:
            return self._login_status

    @property
    def connection(self):
        with self._connection_lock:
            return self._connection

    @connection.setter
    def connection(self, value):
        with self._connection_lock:
            self._connection = value
    """

    @property
    def messages_connection(self):
        with self._messages_connection_lock:
            return self._messages_connection

    @messages_connection.setter
    def messages_connection(self, value):
        with self._messages_connection_lock:
            self._messages_connection = value
    """
    def login(self, username, password, callback):
        self.connection = socket.socket()
        self.connection.connect(SERVER_ADDRESS)
        self.listen_to_user_thread = threading.Thread(
            target=self.receive_message)

        self.listen_to_user_thread.start()
        print("sending info")
        #TODO: #(str(len(msg)).encode() + b"-" + msg)
        msg = f"04{username}#{password}#".encode()
        self.send_message(msg)

        #TODO: manage the messages correctly (add index to messages)
        while True:
            with self.messages_lock:
                if len(self.messages) > 0:
                    with self._login_status_lock:
                        self._login_status = self.messages.pop()
                        break
                    #TODO: manage all cases (wrong password etc..)

        Clock.schedule_once(callback)
        #TODO: put None in logging thread if it crashes or Logged out

    def send_message(self, msg):
        self.connection.sendall(str(len(msg)).encode() + b"-" + msg)

    def receive_message(self):
        while True:
            length = ""
            total_got = 0
            msg = ""
            data = self.connection.recv(1).decode()
            while not data == "-":
                length += data
                data = self.connection.recv(1).decode()
            while total_got < int(length):
                data = self.connection.recv(1).decode()
                msg += data
                total_got += 1
            print(msg)
            with self.messages_lock:
                self.messages.append(msg)

    def build(self):
        return


def main():
    MathematifunApp().run()


if __name__ == '__main__':
    main()
