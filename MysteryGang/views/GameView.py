from datetime import datetime
import json
from random import random, shuffle

import arcade
from arcade.gui import UIManager

from MysteryGang.gui import CluePane, MediaPane, ChatPane, AppPane
from ..constants import ASSET_PREFIX, MUSIC_PREFIX, SPEED, CLUE_PREFIX, BORDER_WIDTH
from ..resources import Location, Investigator

SPRITE_SIZE = 60

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


class LocationSprite(arcade.SpriteSolidColor):
    """investiator sprite object"""

    def __init__(self, location, w, h, color=None):
        self.location = location
        if color is None:
            color = arcade.color.GRAY
        super().__init__(w, h, color)


class WorkerSprite(arcade.Sprite):
    """investiator sprite object"""

    locked = False

    def __init__(self, worker):
        self.worker = worker
        path = CLUE_PREFIX.format(worker)
        super().__init__(path)


class GameView(arcade.View):
    """Main view for test game."""

    def __init__(self):
        super().__init__()
        self.panes = []
        self.locations = []
        self.locationSprites = arcade.SpriteList()
        self.workerSprites = arcade.SpriteList()
        self.investigators = []
        self.ui_manager = UIManager()
        self.media_player = arcade.Sound(
            MUSIC_PREFIX.format('broken_loop_3.ogg')).play(loop=True)

        self.heldLocations = []
        self.heldWorker = None

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

        clues = data['clues']
        # Generate delays between 0.5 and 12 hours (expressed in seconds)
        delays = sorted([random() * 41400 + 1800 for clue in data['clues']])
        # Randomize which locations we'll use
        locations = list(data['locations'].items())
        shuffle(locations)
        # Assign delays and clues to locations. The clues should have delays
        # in increasing order. This is because clues later in the list are
        # considered more useful and require more time to find.
        for delay, clue, (name, location) in zip(delays, clues, locations):
            self.locations.append(Location(
                name, delay * SPEED, clue, **location))
        for name, investigator in data['investigators'].items():
            self.investigators.append(Investigator(
                self.chat_pane, name, **investigator))

        spacing = (height - BORDER_WIDTH * 2) / 6
        for pos, loc in enumerate(self.locations):
            ls = LocationSprite(loc, SPRITE_SIZE, SPRITE_SIZE)
            ls.center_x = 3 * width / 5
            ls.center_y = height - spacing * pos - SPRITE_SIZE / 2 - BORDER_WIDTH * 2
            self.locationSprites.append(ls)

        starter_worker = 'BrianDelight112.png'
        ws = WorkerSprite(starter_worker)
        ws.center_x = 2 * width / 5
        ws.center_y = height - 100
        self.workerSprites.append(ws)

    def on_draw(self):
        """Render the screen."""
        # This command should happen before we start drawing. It will clear the
        # screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        for pane in self.panes:
            pane.on_draw()
        self.locationSprites.draw()
        self.workerSprites.draw()

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
        # Update each investigator's countdown
        for investigator in self.investigators:
            if investigator.countdown and investigator.countdown > 0:
                investigator.countdown -= delta_time

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
        elif is_ctrl and key == arcade.key.E:  # Force EndingView for testing
            ending = self.window.ending_view
            self.ui_manager.unregister_handlers()
            self.window.show_view(ending)
        else:
            key_val = 'not mapped yet'

        if self.window.dump_keys:
            print(f"'{key_val}'")

    def on_key_release(self, key, key_modifiers):
        """Called whenever the user lets off a previously pressed key."""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """Called whenever the mouse moves."""

        if self.heldWorker:
            self.heldWorker.center_x += dx
            self.heldWorker.center_y += dy

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        now = datetime.now()
        print('pressed x:{} y:{} @ {}'.format(x, y, now))

        hit_workers = arcade.get_sprites_at_point((x, y), self.workerSprites)
        if len(hit_workers) == 1 and not hit_workers[0].locked:
            self.heldWorker = hit_workers[0]
            self.worker_start_pos_x = self.heldWorker.center_x
            self.worker_start_pos_y = self.heldWorker.center_y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when the user unpresses a mouse button."""

        if self.heldWorker:
            hits = self.heldWorker.collides_with_list(self.locationSprites)
            print(hits)
            if hits:
                self.chat_pane.recv_msg('Brian', 'I am going to the location')
                self.heldWorker.locked = True
            else:
                self.heldWorker.center_x = self.worker_start_pos_x
                self.heldWorker.center_y = self.worker_start_pos_y

        self.heldWorker = None
