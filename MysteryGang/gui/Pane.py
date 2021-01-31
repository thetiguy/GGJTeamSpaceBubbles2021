import arcade

from ..constants import BORDER_WIDTH


class Pane:
    """A simple rectangular pane with a border."""

    background_color = arcade.color.WHITE
    border_color = arcade.color.BLACK
    border_width = BORDER_WIDTH

    def __init__(self, left, right, top, bottom, background_color=None,
                 border_color=None, border_width=None):
        self.resize(left, right, top, bottom)

        if background_color is not None:
            self.background_color = background_color
        if border_color is not None:
            self.border_color = border_color
        if border_width is not None:
            self.border_width = border_width

    def on_draw(self):
        """Draw this panel, thicker at top."""

        buff = self.border_width / 2
        # Draw the border of the pane
        arcade.draw_lrtb_rectangle_outline(
            self.left + buff,
            self.right - buff,
            self.top - buff,
            self.bottom + buff,
            self.border_color,
            self.border_width)
        # Draw box background
        arcade.draw_lrtb_rectangle_filled(
            self.left + buff,
            self.right - buff,
            self.top - self.border_width,
            self.bottom + buff,
            self.background_color)

    def resize(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
