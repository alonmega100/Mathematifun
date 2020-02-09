"""
The login screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App

class LoginScreen(Screen):
    """
    The login screen
    """
    login_button = ObjectProperty(None)
    username_text_input = ObjectProperty(None)
    def on_login_button_press(self, _):
        """
        Login to server
        :param _:
        :return:
        """
        app = App.get_running_app()
        # app.connection.connect()
