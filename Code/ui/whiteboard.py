from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class Whiteboard(Widget):
    settings = ObjectProperty()
    board = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def start(self):
        self.settings.clear_button.bind(
            on_press=lambda _: self.board.canvas.clear())
