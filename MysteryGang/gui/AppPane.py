import arcade

from . import Pane
from ..constants import FONTS


class AppPane(Pane):
    """A panel that will look and act sort of like hangouts."""


    def __init__(self, left, right, top, bottom, ui_manager):
        """Set up the App section of the game screen."""
        super().__init__(left, right, top, bottom,
                         background_color=arcade.color.ANTI_FLASH_WHITE,
                         border_color=arcade.color.ROYAL_PURPLE)
        self.ui_manager = ui_manager
