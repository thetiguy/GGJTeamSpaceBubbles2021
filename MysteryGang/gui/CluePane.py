from arcade.gui import UIFlatButton

from ..constants import FONTS
from . import Pane

CLUE_HEIGHT = 16


class ClueButton(UIFlatButton):
    def __init__(self, text, center_x, center_y, width, height, align,
                 media_pane):
        super().__init__(text, center_x, center_y, width, height, align)
        self.text = text
        self.media_pane = media_pane

    def on_click(self):
        self.media_pane.display(self.text)


class CluePane(Pane):
    """A pane that display an image."""

    def __init__(self, left, right, top, bottom, ui_manager, media_pane, clues):
        self.buttons = []
        super().__init__(left, right, top, bottom)

        # Create the clue buttons
        for i, clue in enumerate(clues):
            button = ClueButton(
                clue, self.center_x, self.center_y - CLUE_HEIGHT * i,
                self.width, CLUE_HEIGHT, 'left', media_pane)
            button.set_style_attrs(font=FONTS, font_size=12)
            ui_manager.add_ui_element(button)
            self.buttons.append(button)

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)

        # Gotta account for the 1 px border and some whitespace
        self.height = self.top - self.bottom - 4
        self.width = self.right - self.left
        self.center_x = self.left + (self.width) // 2
        self.center_y = self.top - CLUE_HEIGHT // 2

        for i, button in enumerate(self.buttons):
            button.center_x = self.center_x
            button.center_y = self.center_y - CLUE_HEIGHT * i
            button.width = self.width
