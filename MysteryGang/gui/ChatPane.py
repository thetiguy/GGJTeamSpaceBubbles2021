from datetime import datetime
import math

import arcade

from . import Pane
from ..constants import FONTS, MUSIC_PREFIX
from ..resources import Investigator

MESSAGE_LINE_HEIGHT = 40


class ChatPane(Pane):
    """A panel that will look and act sort of like hangouts."""

    messages = []
    send_box = None
    player_worker = None
    scroll_offset = 0

    def __init__(self, left, right, top, bottom, ui_manager):
        """Set up the Chat section of the game screen."""
        super().__init__(left, right, top, bottom,
                         background_color=arcade.color.ANTI_FLASH_WHITE,
                         border_color=arcade.color.DARK_PASTEL_GREEN)
        self.ui_manager = ui_manager

        buff = self.border_width / 2
        send_left = self.left + buff
        send_right = self.right - buff
        send_bottom = self.bottom
        send_top = send_bottom + MESSAGE_LINE_HEIGHT
        self.send_box = ChatBox(send_left, send_right, send_top, send_bottom)
        inside_height = top - bottom - self.border_width * 2
        msg_slots = int(inside_height / (MESSAGE_LINE_HEIGHT + 4))
        self.max_msg_count = msg_slots - 1  # account for send box
        self.player_worker = Investigator(self, None, 'Player', None, None)

    def resize(self, left, right, top, bottom):
        super().resize(left, right, top, bottom)
        buff = self.border_width / 2
        send_left = self.left + buff
        send_right = self.right - buff
        send_bottom = self.bottom
        send_top = send_bottom + 40
        if self.send_box is not None:
            self.send_box.resize(send_left, send_right, send_top, send_bottom)
        inside_height = top - bottom - self.border_width * 2
        msg_slots = int(inside_height / (MESSAGE_LINE_HEIGHT + 4))
        self.max_msg_count = msg_slots - 1  # account for send box

    def send_key(self, key):
        """Handles keys from main UI."""
        self.send_box.send_key(key)

    def show_msg_buffer(self):
        msg = self.send_box.get_current_msg()
        print(f'[{msg}]')

    def send_msg_buffer(self):
        msg = self.send_box.get_current_msg()
        self.show_msg_buffer()
        self.send_msg('Worker', msg)
        self.send_box.clear()

    def send_msg(self, target, message):
        """Send a message from the chat to a worker."""
        self.messages.append(ChatMessage(self.player_worker, target, message))
        arcade.Sound(MUSIC_PREFIX.format('sfx_send_message.ogg')).play()

    def recv_msg(self, source, msg, attachment=None):
        """place a message from a working into the chat."""
        self.messages.append(ChatMessage(source, self.player_worker, msg, attachment))
        arcade.Sound(MUSIC_PREFIX.format('sfx_text_notification.ogg')).play()
        print('Ding!')

    def on_draw(self):
        """Draw the chat box elements."""
        super().on_draw()
        self.send_box.on_draw()
        text_color = arcade.color.BLACK

        start_pos = self.send_box.top
        n = 1
        # build chat bloops from bottom up, will solve most issues

        msg_pool = self.messages
        if self.scroll_offset > 0:
            calc_offset = max(self.scroll_offset, 10)
            msg_pool = self.messages[:self.scroll_offset]
        for cm in reversed(msg_pool):
            # calc stuff
            if cm.sender == self.player_worker:
                left = self.left + 100
                color = arcade.color.GRAY
                box_width = 40
            else:
                left = self.left + self.border_width + 30
                color = arcade.color.WHITE
                box_width = 34

            right = self.right - self.border_width
            lines = math.ceil(len(cm.text) / box_width)

            height = MESSAGE_LINE_HEIGHT * lines
            padded_line_height = (MESSAGE_LINE_HEIGHT + 4)

            bottom = start_pos - self.border_width - 5 + n * padded_line_height
            top = bottom + height

            msg_lines = []
            if lines > 1:  # insert newlines
                words = cm.text.split()
                while len(words) > 0:
                    chunk = ''
                    while len(chunk) < box_width - 5 and len(words) > 0:
                        chunk = chunk + ' ' + words.pop(0)
                    msg_lines.append(chunk)
                text = '\n\n'.join(msg_lines)
            else:
                text = cm.text

            if top > self.top - self.border_width:
                break
            # draw rect
            arcade.draw_lrtb_rectangle_filled(
                left, right, top, bottom, color)

            # draw icon (if worker)
            if cm.sender != self.player_worker:
                arcade.draw_circle_filled(left - 15, top - 15, 15,
                                          cm.sender.color)

            # draw words
            arcade.draw_text(text,
                             left + 4,
                             bottom + 4,
                             text_color, font_size=16, font_name=FONTS,
                             anchor_x="left", anchor_y="bottom")
            n = n + lines


class ChatBox(Pane):
    """User types messages here"""

    content = []

    def __init__(self, left, right, top, bottom):
        """Set up the Chat section of the game screen."""
        super().__init__(left, right, top, bottom,
                         background_color=arcade.color.WHITE,
                         border_color=arcade.color.DARK_GRAY,
                         border_width=4)

    def send_key(self, key):
        self.content.append(key)

    def clear(self):
        self.content = []

    def get_current_msg(self):
        return ''.join(self.content)

    def on_draw(self):
        """Draw the chat box elements."""
        super().on_draw()

        text_color = arcade.color.BLACK
        text = self.get_current_msg()

        if text == '':
            text = 'Send a message'
            text_color = arcade.color.DARK_GRAY

        arcade.draw_text(text,
                         self.left + self.border_width,
                         self.bottom + self.border_width,
                         text_color, font_size=18, font_name=FONTS,
                         anchor_x="left", anchor_y="bottom")


class ChatMessage:
    """Representation of a message in a chat."""

    text = ''
    time = None
    sender = None
    receiver = None
    attachement = None

    def __init__(self, sender, target, message, attachemnt=None):
        self.time = datetime.now()
        self.text = message
        self.attachemnt = attachemnt
        self.sender = sender
        self.receiver = target

    def chat_string(self):
        if self.attachemnt is None:
            extra = ''
        else:
            extra = '&'
        return f'{self.time} {self.sender.name}->{self.receiver}: {self.text} {extra}'  # NOQA
