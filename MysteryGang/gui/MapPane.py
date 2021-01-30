import arcade

from . import Pane


class MapPane(Pane):
    """A pane that display an image."""

    def __init__(self, left, right, top, bottom):
        super().__init__(left, right, top, bottom)

        # Load the image for the map
        self.map = arcade.load_texture('assets/art/maps/map.png')

    def on_draw(self):
        super().on_draw()

        # Draw the map
        arcade.draw_lrwh_rectangle_textured(
            self.bottom_left_x, self.bottom_left_y, self.width, self.height,
            self.map)

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)

        # Coordinates for the map! It's a different coordinate system than used
        # for drawing the pane. I find your lack of consistency disturbing.
        self.bottom_left_x = self.left + 1  # Gotta account for the 1px border
        self.bottom_left_y = self.bottom + 1
        self.height = self.top - self.bottom - 2
        self.width = self.right - self.left - 2
