from datetime import datetime
import json

import arcade
from arcade.gui import UIManager

from MysteryGang.gui import CluePane, MediaPane, ChatPane, AppPane
from ..constants import ASSET_PREFIX, BORDER_WIDTH, MUSIC_PREFIX
from ..resources import Location, Investigator

# A temporary hardcoding of clues
CLUES = [
    'map.png',
    'ThankYouButWhy.wav',
    'BrianDelight112.png',
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
    """Main view for test game."""

    def __init__(self):
        super().__init__()
        self.panes = []
        self.locations = []
        self.investigators = []
        self.ui_manager = UIManager()
        self.media_player = arcade.Sound(
            MUSIC_PREFIX.format('broken_loop_3.ogg')).play(loop=True)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CYAN)

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        width, height = self.window.get_size()

        self.media_pane = MediaPane(  # top left
            1, width / 3, height, height / 2, 'map.png')
        self.clue_pane = CluePane(  # Bottom Left
            1, width / 3, height / 2, 1, self.ui_manager, self.media_pane)
        self.clue_pane.add_clue(*CLUES)
        self.app_pane = AppPane(  # Middle 1/3
            width / 3, 2 * width / 3, height, 1, self.ui_manager)
        self.chat_pane = ChatPane(  # Right 1/3
            (2 * width) / 3, width - 1, height, 1, self.ui_manager)
        self.panes = [
            self.clue_pane, self.media_pane, self.chat_pane, self.app_pane]

        # Load the locations and investigators from file
        with open(ASSET_PREFIX.format('resources.json')) as f:
            data = json.load(f)
        for name, location in data['locations'].items():
            self.locations.append(Location(name, **location))
        for name, investigator in data['investigators'].items():
            self.investigators.append(Investigator(
                self.chat_pane, name, **investigator))

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
        self.media_pane.resize(1, width / 3, height, height / 2)
        self.clue_pane.resize(1, width / 3, height / 2, 1)
        self.app_pane.resize(width / 3, 2 * width / 3, height, 1)
        self.chat_pane.resize(2 * width / 3, width - 1, height, 1)

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
        if self.window.dump_keys:
            print(f'key: {key}, modifiers: [{key_modifiers}]')

        is_cap = (key_modifiers & arcade.key.MOD_SHIFT or
                  key_modifiers & arcade.key.MOD_CAPSLOCK)
        is_ctrl = key_modifiers & arcade.key.MOD_CTRL
        if key < 126 and not is_ctrl:  # ASCII press, ignore ESC
            key_val = chr(key)
            if is_cap:
                key_val = key_val.upper()
            self.chat_pane.send_key(key_val)
        elif key in [arcade.key.ENTER, arcade.key.NUM_ENTER]:
            key_val = 'Enter'
            self.chat_pane.send_msg_buffer()
        elif key == arcade.key.ESCAPE:
            pause = self.window.pause_view
            # hide ui elements, call register_handlers to reverse
            self.ui_manager.unregister_handlers()
            self.window.show_view(pause)
        else:
            key_val = 'not mapped yet'

        if self.window.dump_keys:
            print(f"'{key_val}'")

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
