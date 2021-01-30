import arcade

from . import Pane
from ..constants import CLUE_PREFIX


class MediaPane(Pane):
    """A pane that display an image."""

    def __init__(self, left, right, top, bottom, volume, asset):
        super().__init__(left, right, top, bottom)

        self.display(asset)
        self.volume = volume

    def display(self, asset):
        path = CLUE_PREFIX.format(asset)
        ext = asset[-3:]
        if ext == 'wav':
            arcade.Sound(path).play(self.volume)
        elif ext == 'png':
            self.media = arcade.load_texture(path)

    def on_draw(self):
        super().on_draw()

        # Draw the media
        arcade.draw_lrwh_rectangle_textured(
            self.bottom_left_x, self.bottom_left_y, self.width, self.height,
            self.media)

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)

        # Coordinates for the media! It's a different coordinate system than
        # for drawing the pane. I find your lack of consistency disturbing.
        self.bottom_left_x = self.left + 1  # Gotta account for the 1px border
        self.bottom_left_y = self.bottom + 1
        self.height = self.top - self.bottom - 2
        self.width = self.right - self.left - 2
