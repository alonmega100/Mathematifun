"""
The login screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App

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

    def on_login_button_press(self, str):
        """
        Login to server
        :param _:
        :return:
        """
        app = App.get_running_app()
        app.connection = socket.socket()
        app.connection.connect(SERVER_ADDRESS)
        app.listen_to_user_thread = threading.Thread(
            target=MathematifunApp.receive_message, args=(app,))
        app.listen_to_user_thread.start()
        username = self.username_text_input.text
        password = self.password_text_input.text
