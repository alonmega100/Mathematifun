"""
Responsible
"""

__author__ = "Alon Malka"

from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import ObjectProperty


class Chat(RelativeLayout):
    """
    Send the keyboard state through a socket
    """
    content_text_input = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_message(self):
        """
        Sends message to room
        :return:
        """
        content = self.content_text_input.text
        app = App.get_running_app()
        msg = f"07#{content}".encode()
        app.send_message(msg)
