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


import socket
import threading
import logging
import time
import random


import socket
import ui


# TODO ^^^^^^^^^^^^^

WHITEBOARD_FILENAME = "whiteboard.png"


class MathematifunApp(App):
    """
    The big app
    """
    listen_to_user_thread = ObjectProperty(None)
    my_messages = ListProperty()
    room_id = StringProperty()
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

    def on_whiteboard_available(self, *args):
        return

    def login(self, username, password, callback):
        self.connection = socket.socket()
        self.connection.connect((self.server_ip, self.server_port))
        self.listen_to_user_thread = threading.Thread(
            target=self.receive_message)

        self.listen_to_user_thread.start()
        print("sending info")
        # TODO: #(str(len(msg)).encode() + b"-" + msg)
        msg = f"04{username}#{password}#".encode()
        self.send_message(msg)

        # TODO: manage the messages correctly (add index to messages)
        while True:
            time.sleep(0)
            with self.messages_lock:
                if len(self.messages) > 0:
                    with self._login_status_lock:
                        self._login_status = self.messages.pop()[2:]
                        break
                    # TODO: manage all cases (wrong password etc..)

        Clock.schedule_once(callback)
        # TODO: put None in logging thread if it crashes or Logged out

    def send_message(self, msg):
        self.connection.sendall(str(len(msg)).encode() + b"-" + msg)

    @mainthread
    def _add_message_to_my_messages(self, msg):
        print("Added massage to my_messages:", msg)
        self.my_messages.append(msg)
        print(self.my_messages)

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
            else:
                with self.messages_lock:
                    self.messages.append(msg.decode())


def main():
    MathematifunApp().run()


if __name__ == '__main__':
    main()
