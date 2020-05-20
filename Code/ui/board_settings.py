from kivy.uix.gridlayout import GridLayout
from kivy.properties import (DictProperty,
                             ObjectProperty,
                             OptionProperty)

COLORS = {
    "white": (1, 1, 1),
    "Gray": (0.3, 0.3, 0.3),
    "Black": (0, 0, 0),
    "Red": (1, 0, 0),
    "Green": (0, 1, 0),
    "Blue": (0, 0, 1),
    "Yellow": (1, 1, 0)
}
DEFAULT_COLOR = "Black"
WIDTHS = {
    "Tiny": 3,
    "Small": 5,
    "Normal": 10,
    "Big": 35,
    "Huge": 75,
    "Humongous": 200
}
DEFAULT_WIDTH = "Normal"


class BoardSettings(GridLayout):
    colors = DictProperty(COLORS)
    widths = DictProperty(WIDTHS)
    clear_button = ObjectProperty()
    line_color = OptionProperty(
        COLORS[DEFAULT_COLOR],
        options=COLORS.values())
    line_width = OptionProperty(
        WIDTHS[DEFAULT_WIDTH],
        options=WIDTHS.values())

    def set_line_color(self, line_color):
        self.line_color = self.colors[line_color]

    def set_line_width(self, line_width):
        self.line_width = self.widths[line_width]
