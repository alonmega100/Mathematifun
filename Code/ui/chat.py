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
        self._keyboard = None

    def _on_keyboard_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "enter":
            self.send_message()
            return True
        return False

    def _on_keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_key_down)
        self._keyboard = None

    def show_keyboard(self):
        if self._keyboard is not None:
            return

        self._keyboard = Window.request_keyboard(
            self._on_keyboard_close, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_key_down)



    def hide_keyboard(self):
        """
        Hide and close the keyboard.
        """
        if self._keyboard is not None:
            self.keyboard.release()

    def send_message(self):

        content = self.content_text_input.text
        app = App.get_running_app()
        msg = f"07#{content}".encode()
        app.send_message(msg)