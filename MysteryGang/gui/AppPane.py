import arcade

from . import Pane


class AppPane(Pane):
    """A panel that will look and act sort of like hangouts."""

    def __init__(self, left, right, top, bottom, ui_manager):
        """Set up the App section of the game screen."""
        super().__init__(left, right, top, bottom,
                         background_color=arcade.color.AFRICAN_VIOLET,
                         border_color=arcade.color.ROYAL_PURPLE)
        self.ui_manager = ui_manager
