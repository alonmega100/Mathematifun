"""
The main screen
"""


__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App


class MainScreen(Screen):
    """
    The main screen
    """
    messages_label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.bind(
            my_messages=lambda _, value: self.update_messages_label(value))

    def create_room(self):
        app = App.get_running_app()
        app.send_message(b"05")

    def update_messages_label(self, messages):
        if len(messages) >= 10:
            messages.pop(0)
        final = ""
        for message in messages:
            author = message[:message.find("#")]
            text = message[message.find("#") + 1:]
            final += author + ": " + text + "\n"
        self.messages_label.text = "Messages you got:\n" + final
