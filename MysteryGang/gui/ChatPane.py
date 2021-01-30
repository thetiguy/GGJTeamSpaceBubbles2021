from datetime import datetime

from . import Pane

class ChatPane(Pane):
    """A panel that will look and act sort of like hangouts."""

    chat_buffer = []
    messages = []

    def __init__(self, left, right, top, bottom, ui_manager):
        super().__init__(left, right, top, bottom)

    def send_key(self, key):
        """Handles keys from main UI."""
        self.chat_buffer.append(key)

    def show_msg_buffer(self):
        msg = ''.join(self.chat_buffer)
        print(f'[{msg}]')

    def send_msg_buffer(self):
        msg = ''.join(self.chat_buffer)
        self.show_msg_buffer()
        self.send_msg('Worker', msg)
        self.chat_buffer = []

    def send_msg(self, target, message):
        """Send a message from the chat to a worker."""
        self.messages.append(ChatMessage('Player', target, message))
        # update worker
        # update chat window
        self.render_messages()

    def recv_msg(self, source, message, attachment=None):
        """place a message from a working into the chat."""
        self.messages.append(ChatMessage(target, 'Player', message, attachment))
        # Update worker
        # Do clue work
        # Do map work
        # update chat window

    def render_chat_input(self):
        pass

    def render_messages(self):
        """display messages in the chat window."""

        print('-----------------------')
        for m in self.messages:
            print(f'{m.chat_string()}')
        print('-----------------------')

class ChatBox(Pane):
    """User types messages here"""
    pass

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
        if self.attachemnt == None:
            extra = ''
        else:
            extra = '&'
        return f'{self.time} {self.sender}->{self.receiver}: {self.text} {extra}'


