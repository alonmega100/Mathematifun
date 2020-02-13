"""
The main!!! Big main1!!!!
"""

__author__ = "Alon"


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import socket
import ui

import whiteboard_screen
import send_message_screen
import main_screen
import signup_screen
import login_screen
# TODO ^^^^^^^^^^


class MathematifunApp(App):
    """
    The big app
    """
    connetion = ObjectProperty(socket.socket)

    def build(self):
        return Builder.load_file("Mathematifun.kv")


def main():
    MathematifunApp().run()


if __name__ == '__main__':
    main()
