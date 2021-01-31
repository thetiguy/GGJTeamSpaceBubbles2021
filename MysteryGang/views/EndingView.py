import arcade
from arcade.gui import UIManager

from ..constants import FONTS


class EndingView(arcade.View):
    """Ending / Credits view for the game. """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()
        self.won = True

    def on_show(self):
        self.setup()

        # TODO: Remove before submitting game
        if self.won:
            backcolor = arcade.color.WHITE
        else:
            backcolor = arcade.color.BLACK

        arcade.set_background_color(backcolor)
        self.window.switch_music('credits.ogg')

    def on_draw(self):
        width, height = self.window.get_size()

        arcade.start_render()

        # TODO: Remove before submitting game
        if self.won:
            text = "LIFE!!!"
            textcolor = arcade.color.GREEN
        else:
            text = "DEATH!"
            textcolor = arcade.color.RED

        for i in range(0, 4):
            arcade.draw_text(
                text, width / 2-i, height / 2 + 50-i, arcade.color.WHITE,
                font_name=FONTS, font_size=50, anchor_x="center")

            arcade.draw_text(
                'Press spacebar to continue', width / 2 - i, height / 2 - i,
                arcade.color.WHITE, font_name=FONTS, font_size=20,
                anchor_x='center')

        arcade.draw_text(
            text, width / 2, height / 2 + 50, textcolor,
            font_name=FONTS, font_size=50, anchor_x="center")

        arcade.draw_text(
            "Press spacebar to continue", width / 2, height / 2, textcolor,
            font_name=FONTS, font_size=20, anchor_x="center")

    def setup(self):
        """Set up this view."""
        self.ui_manager.purge_ui_elements()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:
            self.ui_manager.purge_ui_elements()
            self.game_view.ui_manager.register_handlers()
            self.window.show_view(self.game_view)
