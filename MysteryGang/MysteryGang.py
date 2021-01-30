from datetime import datetime

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "wooooo"


class GameView(arcade.View):
    """Main window for test game."""

    def __init__(self):
        super().__init__()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CYAN)

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """Render the screen."""

        # This command should happen before we start drawing. It will clear the
        # screen to the background color, and erase what we drew last frame.
        arcade.start_render()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """Called whenever the user lets off a previously pressed key."""
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        now = datetime.now()
        print('pressed x:{} y:{} @ {}'.format(x, y, now))

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when the user unpresses a mouse button."""
        pass


class OpeningView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CELESTIAL_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Welcome", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to go", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


class EndingView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

def main():
    """Main method"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    intro_view = OpeningView()
    window.show_view(intro_view)

    arcade.run()


if __name__ == "__main__":
    main()

