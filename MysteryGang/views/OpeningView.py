import arcade

from . import GameView


class OpeningView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CELESTIAL_BLUE)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        width, height = self.window.get_size()

        arcade.draw_text("Welcome", width / 2, height / 2,
                         arcade.color.WHITE, font_size=50,
                         font_name=['Arial', 'DejaVuSans'],
                         anchor_x="center")

        arcade.draw_text("Click to go", width / 2, height / 2-75,
                         arcade.color.WHITE, font_size=50,
                         font_name=['Arial', 'DejaVuSans'],
                         anchor_x="center")
