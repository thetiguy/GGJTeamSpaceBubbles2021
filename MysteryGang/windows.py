import arcade

from .views import OpeningView, GameView, PauseView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MysteryGangWindow(arcade.Window):
    """Main Game Window."""

    dump_keys = False

    def __init__(self, width, height, title, resizable):
        super().__init__(width, height, title, resizable=resizable)

        # init views
        self.intro_view = OpeningView()
        self.game_view = GameView()
        self.pause_view = PauseView(self.game_view)
        # self.end_view = EndView()

        self.show_view(self.intro_view)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        is_ctrl = modifiers & arcade.key.MOD_CTRL
        if key == arcade.key.F11:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        elif is_ctrl and key == arcade.key.W:  # exit
            self.close()
        elif is_ctrl and key == arcade.key.P:  # print every keypress
            self.dump_keys = not self.dump_keys
        elif is_ctrl and key == arcade.key.T:  # force worker message
            if self.current_view == self.game_view:
                msg = 'Hello, I found a thing'
                self.game_view.chat_pane.recv_msg('Worker', msg)

        if self.current_view == self.intro_view:
            self.start_game()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_view == self.intro_view:
            self.start_game()

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""
        super().on_resize(width, height)

    def on_show(self):
        """This is run once when we switch to this view."""
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def start_game(self):
        self.game_view.setup()
        self.show_view(self.game_view)
