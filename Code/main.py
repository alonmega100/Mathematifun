"""
The main!!! Big main1!!!!
"""

__author__ = "Alon"


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import socket
import ui


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
