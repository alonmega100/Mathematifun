import io
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import (NumericProperty,
                             ListProperty)
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.image import Image

DEFAULT_COLOR = (1, 1, 1)
DEFAULT_WIDTH = 30


class Board(Image):
    line_color = ListProperty(DEFAULT_COLOR)
    line_width = NumericProperty(DEFAULT_WIDTH)

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self._update_image_file)
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.bind(on_whiteboard_available=self._redraw_image_canvas)

    def _redraw_image_canvas(self, *_):
        self.reload()
        print("CANVAS UPDATED")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.line_color)
                d = self.line_width
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=d)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if "line" in touch.ud:
                touch.ud["line"].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._trigger()

    def _update_image_file(self, _):
        app = App.get_running_app()
        image = self.export_as_image()
        image.save(app.whiteboard_filename)
        image_data = io.BytesIO()
        image.save(image_data, fmt="png")
        app.send_message(b"08#" + image_data.read())
