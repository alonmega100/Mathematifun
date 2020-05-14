from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import (NumericProperty,
                             ListProperty)
from kivy.clock import Clock
from kivy.app import App

DEFAULT_COLOR = (1, 1, 1)
DEFAULT_WIDTH = 30


class Board(StencilView):
    line_color = ListProperty(DEFAULT_COLOR)
    line_width = NumericProperty(DEFAULT_WIDTH)

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.update_canvas)
        super().__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='img.png', pos=self.pos,
                                size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)
        #Clock.schedual_interval(lambda _: self.bg.reload(), 0.1)
        app = App.get_running_app()
        app.bind(on_image_available=self.update_canvas)

    def update_canvas(self, is_available):
        if not is_available:
            return
        self.canvas.remove(self.bg)
        with self.canvas:
            
            self.bg = Rectangle(source='img.png', pos=self.pos,
                                size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)
        app = App.get_running_app()
        app.image_is_available = False
        print("CANVAS UPDATED ")


    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

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
        self._trigger()

    def update_canvas(self, _):
        self.export_to_png(filename='img.png')
        app = App.get_running_app()
        with open("img.png", 'rb') as canvas_png:
            app.send_message(b"08#" + canvas_png.read())
