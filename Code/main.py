"""
The main
"""

__author__ = "Alon"


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty


import socket
import threading
import logging
import time
import random


import socket
import ui

import whiteboard_screen
import send_message_screen
import main_screen
import signup_screen
import login_screen
# TODO ^^^^^^^^^^^^^


class MathematifunApp(App):
    """
    The big app
    """
    listen_to_user_thread = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connection_lock = threading.Lock()
        self.connection = None
        self.messages = []
        self.messages_lock = threading.Lock()

    @property
    def connection(self):
        with self._connection_lock:
            return self._connection

    @connection.setter
    def connection(self, value):
        with self._connection_lock:
            self._connection = value

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
        return Builder.load_file("Mathematifun.kv")


def main():
    MathematifunApp().run()


if __name__ == '__main__':
    main()
