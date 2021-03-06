"""
The login screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from main import StudyTogetherApp
import socket
import threading
import logging
import time
import random


class LoginScreen(Screen):
    """
    The login screen
    """

    login_button = ObjectProperty(None)
    username_text_input = ObjectProperty(None)
    password_text_input = ObjectProperty(None)
    login_status_textbox = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._login_thread = None

    def _end_logging_in(self, _):

        app = App.get_running_app()
        self.login_status_textbox.text = app.login_status
        if app.login_status == "Logged in":
            self.manager.transition.direction = "left"
            app.root.current = "main"
        else:
            self._login_thread = None

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        self._login_thread = None

    def login(self):
        """
        Login to server
        :param:
        :return:
        """

        app = App.get_running_app()
        if self._login_thread is not None:
            return None

        username = self.username_text_input.text
        password = self.password_text_input.text

        self._login_thread = threading.Thread(
            target=app.login,
            args=(username, password, self._end_logging_in))
        self._login_thread.start()
