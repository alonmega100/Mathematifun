"""
The join room screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App


class JoinRoomScreen(Screen):
    """
    The join room screen
    """
    room_id_text_input = ObjectProperty()

    def join_room(self):
        app = App.get_running_app()
        app.room_id = self.room_id_text_input.text
        app.send_message(("06" + self.room_id_text_input.text).encode())
