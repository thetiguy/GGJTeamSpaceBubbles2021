from datetime import datetime

import arcade

from MysteryGang.gui import CluePane, MapPane, Pane

# A temporary hardcoding of clues
CLUES = [
    'first_clue.mp3',
    'second_clue.mp4',
    'third_clue.png',
    'fourth_clue.png',
    'fifth_clue.mp4',
    'sixth_clue.mp3',
    'seventh_clue.mp3',
    'eithth_clue.png',
    'ninth_clue.png',
    'tenth_clue.png'
]


class GameView(arcade.View):
    """Main window for test game."""

    def __init__(self):
        super().__init__()
        self.panes = []

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CYAN)

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        width, height = self.window.get_size()
        self.clue_pane = CluePane(1, width / 3, height - 1, height / 2, CLUES)
        self.map_pane = MapPane(1, width / 3, height / 2, 1)
        self.admin_pane = Pane(width / 3, width - 1, height - 1, 1)
        self.panes = [self.clue_pane, self.map_pane, self.admin_pane]

    def on_draw(self):
        """Render the screen."""
        # This command should happen before we start drawing. It will clear the
        # screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        for pane in self.panes:
            pane.on_draw()

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""
        self.window.on_resize(width, height)
        self.clue_pane.resize(1, width / 3, height - 1, height / 2)
        self.map_pane.resize(1, width / 3, height / 2, 1)
        self.admin_pane.resize(width / 3, width - 1, height - 1, 1)

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
