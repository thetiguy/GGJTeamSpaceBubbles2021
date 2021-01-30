from arcade.gui import UIFlatButton

from ..constants import FONTS
from . import Pane

CLUE_HEIGHT = 25


class ClueButton(UIFlatButton):
    def __init__(self, text, center_x, center_y, width, height, align):
        super().__init__(text, center_x, center_y, width, height, align)
        self.text = text

    def on_click(self):
        print('Clicked {0}'.format(self.text))


class CluePane(Pane):
    """A pane that display an image."""

    def __init__(self, left, right, top, bottom, ui_manager, clues):
        super().__init__(left, right, top, bottom)

        # Create the clue buttons
        for i, clue in enumerate(clues):
            if i == self.max_clues:
                break
            button = ClueButton(
                clue, self.center_x, self.center_y - CLUE_HEIGHT * i,
                self.width, CLUE_HEIGHT, 'left')
            button.set_style_attrs(font=FONTS)
            ui_manager.add_ui_element(button)

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)

        # Gotta account for the 1 px border and some whitespace
        self.height = self.top - self.bottom - 4
        self.width = self.right - self.left
        self.center_x = self.left + (self.width) // 2
        self.center_y = self.top - CLUE_HEIGHT // 2

        # Determine the number of clues that can fit in the pane
        self.max_clues = self.height // CLUE_HEIGHT  # Integer division!
