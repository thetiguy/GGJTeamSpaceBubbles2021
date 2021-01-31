from datetime import datetime
import json
from random import random, shuffle
from types import SimpleNamespace
import math

import arcade
from arcade.gui import UIManager
from pyglet import clock

from MysteryGang.gui import CluePane, MediaPane, ChatPane, AppPane
from ..constants import (ASSET_PREFIX, BORDER_WIDTH, FONTS, GAME_LENGTH,
                         MUSIC_PREFIX, PROFILE_PREFIX, SPEED, SPRITE_SIZE)
from ..resources import Location, Investigator
from ..sprites import LocationSprite, WorkerSprite


# A temporary hardcoding of clues
CLUES = [
    'map1.png'
]
MUSIC_PHASES = [
    'start.ogg',
    'normal.ogg',
    'intense.ogg',
    'timealmostout.ogg'
]


class GameView(arcade.View):
    """Main view for the game."""

    def __init__(self):
        super().__init__()
        self.panes = []
        self.locations = []
        self.locationSprites = arcade.SpriteList()
        self.workerSprites = arcade.SpriteList()
        self.investigators = []
        self.ui_manager = UIManager()

        self.clock_position = None
        self.countdown = None
        self.heldLocations = []
        self.heldWorker = None
        self.location_labels = []
        self.music_phase = 0
        self.music_phase_length = GAME_LENGTH * SPEED / len(MUSIC_PHASES)
        self.started = False
        self.victim = SimpleNamespace(name='Ren', color=(255, 0, 0))

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.CYAN)
        if not self.started:
            self.next_music_phase()
            self.window.media_player.volume = 0.75
            self.started = True
        else:
            self.window.switch_music(MUSIC_PHASES[self.music_phase])

    def next_music_phase(self, delay=None):
        if self.music_phase < len(MUSIC_PHASES):
            self.window.switch_music(MUSIC_PHASES[self.music_phase])
            self.music_phase += 1
            clock.schedule_once(self.next_music_phase, self.music_phase_length)

    def setup(self):
        """Set up the game variables."""
        # Create your sprites and sprite lists here
        width, height = self.window.get_size()

        self.media_pane = MediaPane(  # top left
            1, width / 3, height, height / 2, 'map1.png')
        self.clue_pane = CluePane(  # Bottom Left
            1, width / 3, height / 2, 1, self.ui_manager, self.media_pane)
        self.clue_pane.add_clue(*CLUES)
        self.app_pane = AppPane(  # Middle 1/3
            width / 3, 2 * width / 3, height, 1, self.ui_manager)
        self.chat_pane = ChatPane(  # Right 1/3
            (2 * width) / 3, width - 1, height, 1, self.ui_manager, self)
        self.panes = [
            self.clue_pane, self.media_pane, self.chat_pane, self.app_pane]
        self.clock_position = (width * 0.35, height - BORDER_WIDTH * 2)

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
                self.chat_pane, self.clue_pane, name, **investigator))
        # Load messages
        self.ending_message = data['ending_message']
        self.starting_messages = data['starting_messages']
        self.victim_death_message = data['victim_death']
        # A placeholder to be loaded from json later
        # self.winning_message = data['winning_message']
        self.winning_message = '3 spirals, 5 stars, 0 suns'

        spacing = (height - BORDER_WIDTH * 2) / 6
        for pos, loc in enumerate(self.locations):
            ls = LocationSprite(loc, SPRITE_SIZE, SPRITE_SIZE)
            x = width * 0.51
            y = height - spacing * pos - SPRITE_SIZE / 2 - BORDER_WIDTH * 2
            ls.center_x = x
            ls.center_y = y
            self.locationSprites.append(ls)
            self.location_labels.append((x, y, loc))

        for i, investigator in enumerate(self.investigators):
            ws = WorkerSprite(
                investigator, 0.025, center_x=2 * width / 5,
                center_y=height - 100 * (i + 1))
            self.workerSprites.append(ws)
            investigator.worker_sprite = ws

        clock.schedule_once(self.send_starting_message, random() * 5 + 1, 0)

    def win(self):
        self.countdown = None
        self.chat_pane.recv_msg(self.victim, self.ending_message)
        clock.schedule_once(self.show_ending_view, 10)

    def send_starting_message(self, delay, i):
        message = self.starting_messages[i]
        if message['clue']:
            self.clue_pane.add_clue(message['clue'])
        if i == len(self.starting_messages) - 1:  # Last message
            self.chat_pane.send_msg(
                self.victim.name, message['message'])
            self.countdown = GAME_LENGTH * SPEED
        else:
            self.chat_pane.recv_msg(self.victim, message['message'])
            clock.schedule_once(
                self.send_starting_message, random() * 5 + 1, i + 1)

    def on_draw(self):
        """Render the screen."""
        # This command should happen before we start drawing. It will clear the
        # screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        for pane in self.panes:
            pane.on_draw()
        self.locationSprites.draw()
        bar_bg = arcade.color.GRAY
        bar_fill = arcade.color.DARK_BLUE
        label_color = arcade.color.BLACK
        for x, y, loc in self.location_labels:
            label_x = x + SPRITE_SIZE / 2 + 8
            bar_x = x - SPRITE_SIZE / 2
            arcade.draw_lrtb_rectangle_filled(
                bar_x, bar_x + 200, y - 35, y - 45, bar_bg)

            if loc.countdown:  # Fill progress bar
                percent_complete = 1 - (loc.countdown / loc.delay)
                arcade.draw_lrtb_rectangle_filled(
                    bar_x, bar_x + 200 * percent_complete, y - 35, y - 45,
                    bar_fill)

            label_text = f'{loc.name}\n{loc.element1}\n{loc.element2}'
            arcade.draw_text(
                label_text, label_x, y - 30, label_color, font_size=15,
                font_name=FONTS, anchor_x='left', anchor_y='bottom')
        # Draw countdown Clock
        if self.countdown:
            minutes_left = self.countdown / 60
            hours_left = minutes_left / 60
            h = math.floor(hours_left)
            m = math.floor(minutes_left - 60 * h)
            s = math.floor(self.countdown - (60 * 60 * h) - 60 * m)

            arcade.draw_text(f'{h}:{m}:{s}', *(self.clock_position),
                             label_color, font_size=15, font_name=FONTS,
                             anchor_x='left', anchor_y='bottom')
        self.workerSprites.draw()

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""
        self.window.on_resize(width, height)
        self.media_pane.resize(1, width / 3, height, height / 2)
        self.clue_pane.resize(1, width / 3, height / 2, 1)
        self.app_pane.resize(width / 3, 2 * width / 3, height, 1)
        self.chat_pane.resize(2 * width / 3, width - 1, height, 1)

        spacing = (height - BORDER_WIDTH * 2) / 6
        self.location_labels = []
        self.clock_position = (width * 0.35, height - BORDER_WIDTH * 2)
        for pos, ls in enumerate(self.locationSprites):
            x = width * 0.51
            y = height - spacing * pos - SPRITE_SIZE / 2 - BORDER_WIDTH * 2
            ls.center_x = x
            ls.center_y = y
            self.location_labels.append((x, y, ls.location))

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Update the global countdown
        if self.countdown:
            self.countdown -= delta_time
            if self.countdown < 1:  # Game over
                self.countdown = None
                self.window.ending_view.won = False
                self.chat_pane.recv_msg(self.victim, self.victim_death_message)
                clock.schedule_once(self.show_ending_view, 10)

        # Update each investigator's countdown
        for investigator in self.investigators:
            loc_sprite = investigator.location_sprite
            if (
                loc_sprite and loc_sprite.location and
                loc_sprite.location.countdown and
                loc_sprite.location.countdown > 0
            ):
                loc_sprite.location.countdown -= delta_time

    def show_ending_view(self, delay):
        self.ui_manager.unregister_handlers()
        self.window.show_view(self.window.ending_view)

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

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.chat_pane.left < x < self.chat_pane.right:
            self.chat_pane.scroll_offset = max(
                0, self.chat_pane.scroll_offset + scroll_y)
            print(self.chat_pane.scroll_offset)

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
            arcade.Sound(MUSIC_PREFIX.format('sfx_interface_click.ogg')).play()
            self.heldWorker = hit_workers[0]
            self.worker_start_pos_x = self.heldWorker.center_x
            self.worker_start_pos_y = self.heldWorker.center_y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when the user unpresses a mouse button."""

        if self.heldWorker:
            hits = self.heldWorker.collides_with_list(self.locationSprites)
            if hits and not hits[0].location.occupied:
                self.heldWorker.worker.traverse(hits[0])
                self.heldWorker.locked = True
                hits[0].location.occupied = True
            else:
                self.heldWorker.center_x = self.worker_start_pos_x
                self.heldWorker.center_y = self.worker_start_pos_y

        self.heldWorker = None
