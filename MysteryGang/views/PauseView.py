import arcade
from arcade.gui import UIManager

WIDTH = 800
HEIGHT = 600


class VolumeInput(arcade.gui.UIInputBox):
    def __init__(self,
                 center_x,
                 center_y,
                 width,
                 game_view):
        super().__init__(center_x, center_y, width)
        self.game_view = game_view

    def on_ui_event(self, event):
        if self.text and self.text != '.':
            self.game_view.media_pane.volume = float(self.text)
        super().on_ui_event(event)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.CYAN)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WIDTH / 2,
                         HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         WIDTH / 2,
                         HEIGHT / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Music Volume",
                         WIDTH / 2,
                         HEIGHT / 2 - 69,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        slot = self.window.height / 2
        column_x = self.window.width / 2

        volume_text = str(self.game_view.media_pane.volume)
        ui_input_box = VolumeInput(
            center_x=column_x,
            center_y=slot - 100,
            width=50,
            game_view=self.game_view
        )
        ui_input_box.text = volume_text
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.ui_manager.purge_ui_elements()
            self.game_view.ui_manager.register_handlers()
            self.window.show_view(self.game_view)
        # elif key == arcade.key.ENTER:  # reset game
        #     self.ui_manager.unregister_handlers()
        #     game = self.window.game_view
        #     self.window.show_view(game)
