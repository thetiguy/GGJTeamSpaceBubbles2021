import arcade
from arcade.gui import UIManager

from ..constants import FONTS

VOLUME_SCALE = 100


class VolumeInput(arcade.gui.UIInputBox):
    def __init__(self, center_x, center_y, width, window):
        super().__init__(center_x, center_y, width)
        self.window = window

    def on_ui_event(self, event):
        try:
            self.window.media_player.volume = (float(self.text) / VOLUME_SCALE)
        except ValueError:
            pass
        super().on_ui_event(event)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.CYAN)
        self.window.switch_music('pause.ogg')

    def on_draw(self):
        width, height = self.window.get_size()

        arcade.start_render()

        arcade.draw_text(
            "PAUSED", width / 2, height / 2 + 50, arcade.color.BLACK,
            font_name=FONTS, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text(
            "Press Esc. to return", width / 2, height / 2, arcade.color.BLACK,
            font_name=FONTS, font_size=20, anchor_x="center")
        arcade.draw_text(
            "Music Volume", width / 2, height / 2 - 69, arcade.color.BLACK,
            font_name=FONTS, font_size=15, anchor_x="center")

    def setup(self):
        """Set up this view."""
        self.ui_manager.purge_ui_elements()

        slot = self.window.height / 2
        column_x = self.window.width / 2

        volume_text = str(int(
            self.window.media_player.volume * VOLUME_SCALE))
        ui_input_box = VolumeInput(
            center_x=column_x,
            center_y=slot - 100,
            width=65,
            window=self.window
        )
        ui_input_box.set_style_attrs(font_name=FONTS)
        ui_input_box.text = volume_text
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # Resume the game
            self.ui_manager.purge_ui_elements()
            self.game_view.ui_manager.register_handlers()
            self.window.show_view(self.game_view)
