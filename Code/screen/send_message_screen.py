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
    messages_label = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.bind(
            my_messages=lambda _, value: self.update_messages_label(value))

    def update_messages_label(self, messages):
        if len(messages) >= 10:
            messages.pop(0)
        final = ""
        for message in messages:
            author = message[:message.find("#")]
            text = message[message.find("#") + 1:]
            final += author + ": " + text + "\n"
        self.messages_label.text = "Messages you got:\n" + final

    def on_enter(self, *args):

        pass


    def send_message(self):
        dest = self.destination_user_textbox.text
        content = self.message_textbox.text
        app = App.get_running_app()
        msg = f"03{dest}#{content}".encode()
        app.send_message(msg)
