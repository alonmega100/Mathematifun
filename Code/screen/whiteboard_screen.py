"""
The whiteboard screen
"""

__author__ = "Alon Malka"

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class WhiteboardScreen(Screen):
    """
    The whiteboard screen
    """
    whiteboard = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.whiteboard.start()
