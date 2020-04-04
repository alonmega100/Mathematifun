from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import (NumericProperty,
                             ListProperty)

DEFAULT_COLOR = (1, 1, 1)
DEFAULT_WIDTH = 30


class Board(StencilView):
    line_color = ListProperty(DEFAULT_COLOR)
    line_width = NumericProperty(DEFAULT_WIDTH)

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.line_color)
            d = self.line_width
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud["line"] = Line(points=(touch.x, touch.y), width=d)

    def on_touch_move(self, touch):
        if "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]
