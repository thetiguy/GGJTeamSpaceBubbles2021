import arcade


class Pane:
    """A simple rectangular pane with a border."""

    def __init__(self, left, right, top, bottom):
        self.resize(left, right, top, bottom)

    def on_draw(self):
        # Draw the border of the pane
        arcade.draw_lrtb_rectangle_outline(
            self.left, self.right, self.top, self.bottom, arcade.color.BLACK)

    def resize(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
