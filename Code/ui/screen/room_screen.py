"""
The room screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class RoomScreen(Screen):
    """
    The room screen
    """
    whiteboard = ObjectProperty()
    chat = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.whiteboard.start()

    def on_touch_down(self, touch):
        self.chat.show_keyboard()
        return super().on_touch_down(touch)
