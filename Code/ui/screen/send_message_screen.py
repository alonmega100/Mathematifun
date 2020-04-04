"""
The send a message screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App


class SendMessageScreen(Screen):
    """
    The send message screen
    """
    destination_user_textbox = ObjectProperty()
    message_textbox = ObjectProperty()

    def send_message(self):
        dest = self.destination_user_textbox.text
        content = self.message_textbox.text
        app = App.get_running_app()
        msg = f"03{dest}#{content}".encode()
        app.send_message(msg)
