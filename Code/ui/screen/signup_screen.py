"""
The Sign up screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App

class SignupScreen(Screen):
    """
    The sign up screen
    """
    login_button = ObjectProperty(None)
    username_text_input = ObjectProperty(None)
    password_text_input = ObjectProperty(None)
    login_status_textbox = ObjectProperty()

    def signup(self):
        username = self.username_text_input.text
        password = self.password_text_input.text
        app = App.get_running_app()
        app.send_message(f"09{username}#{password}")
