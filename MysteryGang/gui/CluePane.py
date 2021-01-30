import arcade

from . import Pane

CLUE_HEIGHT = 25


class CluePane(Pane):
    """A pane that display an image."""

    def __init__(self, left, right, top, bottom, clues):
        super().__init__(left, right, top, bottom)
        self.clues = clues

    def on_draw(self):
        super().on_draw()

        # Draw the clues
        for i, clue in enumerate(self.clues):
            if i == self.max_clues:
                break
            arcade.draw_text(
                clue, self.text_left, self.text_top - CLUE_HEIGHT * (i + 1),
                arcade.color.WHITE, font_size=18,
                font_name=['Arial', 'Cantarell-Regular'])

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)

        # Gotta account for the 1 px border and some whitespace
        self.height = self.top - self.bottom - 4
        self.text_left = self.left + 3
        self.text_top = self.top - 3

        # Determine the number of clues that can fit in the pane
        self.max_clues = self.height // CLUE_HEIGHT  # Integer division!
