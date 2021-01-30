from datetime import datetime

import arcade

from . import Pane
from ..constants import FONTS


class ChatPane(Pane):
    """A panel that will look and act sort of like hangouts."""

    messages = []

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
        send_top = send_bottom + 40
        self.send_box = ChatBox(send_left, send_right, send_top, send_bottom)

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
        self.messages.append(ChatMessage('Player', target, message))
        # update worker
        # update chat window
        self.render_messages()

    def recv_msg(self, source, msg, attachment=None):
        """place a message from a working into the chat."""
        self.messages.append(ChatMessage(source, 'Player', msg, attachment))
        # Update worker
        # Do clue work
        # Do map work
        # update chat window
        print('Ding!')
        self.render_messages()

    def render_messages(self):
        """display messages in the chat window."""

        print('-----------------------')
        for m in self.messages:
            print(f'{m.chat_string()}')
        print('-----------------------')

    def on_draw(self):
        """Draw the chat box elements."""
        super().on_draw()
        self.send_box.on_draw()


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
                         text_color, font_size=20, font_name=FONTS,
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
        return f'{self.time} {self.sender}->{self.receiver}: {self.text} {extra}'  # NOQA
