"""
The main screen
"""


__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.app import App


class MainScreen(Screen):
    """
    The main screen
    """
    def create_room(self):
        app = App.get_running_app()
        app.send_message(b"05")
