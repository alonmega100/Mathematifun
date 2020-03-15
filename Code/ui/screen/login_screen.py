"""
The login screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from Code.main import MathematifunApp
import socket
import threading
import logging
import time
import random

SERVER_ADDRESS = ("127.0.0.1", 4261)


class LoginScreen(Screen):
    """
    The login screen
    """
    login_button = ObjectProperty(None)
    username_text_input = ObjectProperty(None)
    password_text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._login_thread = None
        self._login_thread_lock = threading.Lock()

    def _end_logging_in(self, _):
        app = App.get_running_app()
        self.manager.transition.direction = "left"
        app.root.current = "main"

    def _login(self, username, password):
        app = App.get_running_app()
        app.connection = socket.socket()
        app.connection.connect(SERVER_ADDRESS)
        app.listen_to_user_thread = threading.Thread(
            target=app.receive_message)

        app.listen_to_user_thread.start()
        print("sending info")
        #TODO: #(str(len(msg)).encode() + b"-" + msg)
        msg = f"04{username}#{password}#".encode()
        app.connection.sendall(str(len(msg)).encode() + b"-" + msg)

        #TODO: manage the messages correctly (add index to messages)
        while True:
            print("im in the T loop")
            with app.messages_lock:
                print("im in the lock he he")
                if len(app.messages) > 0:
                    print("the len gadol me 0")
                    message = app.messages.pop()
                    if message == "Logged in":
                        print("the message i got:" + message)
                        break
                    #TODO: manage all cases (wrong password etc..)

        Clock.schedule_once(self._end_logging_in)
        #TODO: put None in logging thread if it crashes or Loged out

    def on_login_button_press(self):
        """
        Login to server
        :param:
        :return:
        """
        print("starting the on loging button press function")
        with self._login_thread_lock:
            run = self._login_thread is None
        if run:
            print("getting into RUN (logging button function)")

            username = self.username_text_input.text
            password = self.password_text_input.text
            with self._login_thread_lock:
                print("into the lock")
                self._login_thread = threading.Thread(
                    target=self._login,
                    args=(username, password))
            self._login_thread.start()
