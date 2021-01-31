import arcade
from arcade.gui import UIManager

from ..constants import FONTS, MORTEEVITA

class EndingView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()

    def on_show(self):
        self.setup()

        # TODO: Remove before submitting game
        if MORTEEVITA == False:
            text = "DEATH!"
            backcolor = arcade.color.BLACK
        if MORTEEVITA == True:
            text = "LIFE!!!"
            backcolor = arcade.color.WHITE
            
        arcade.set_background_color(backcolor)

    def on_draw(self):
        width, height = self.window.get_size()

        arcade.start_render()

        # TODO: Remove before submitting game
        if MORTEEVITA == False:
            text = "DEATH!"
            backcolor = arcade.color.BLACK
            textcolor = arcade.color.RED
        if MORTEEVITA == True:
            text = "LIFE!!!"
            backcolor = arcade.color.WHITE
            textcolor = arcade.color.GREEN

        for i in range(0, 4):
            arcade.draw_text(
                text, width / 2-i, height / 2 + 50-i, arcade.color.WHITE,
                font_name=FONTS, font_size=50, anchor_x="center")

            arcade.draw_text(
                "Press spacebar to continue", width / 2-i, height / 2-i, arcade.color.WHITE,
                font_name=FONTS, font_size=20, anchor_x="center")
            
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
