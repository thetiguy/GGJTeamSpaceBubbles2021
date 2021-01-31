from random import random

from pyglet import clock


class Location:
    def __init__(self, name, delay, clue, element1, element2, death_message,
                 success_message, messages):
        self.name = name
        self.delay = delay
        self.clue = clue
        self.element1 = element1
        self.element2 = element2
        self.death_message = death_message
        self.success_message = success_message
        self.messages = messages
        self.occupied = False

        self.frequency = self.delay / len(self.messages) + 1
        self.i = -1

    def get_message(self):
        """Get's an update during the journey.

        If there are no more updates, return None.
        """
        self.i += 1
        return self.messages[self.i] if self.i < len(self.messages) else None


class Investigator:
    def __init__(self, chat_pane, clue_pane, name, color, specialty):
        self.chat_pane = chat_pane
        self.clue_pane = clue_pane
        self.name = name
        self.color = color
        self.specialty = specialty

        self.countdown = None
        self.exhaustion = 1

    def traverse(self, location):
        self.chat_pane.recv_msg(
            self, 'I am going to the {0}'.format(location.name))

        self.location = location
        self.countdown = self.location.delay

        # No, Mr. Bond, I expect you to die!
        rand = random()
        if rand < self.exhaustion / 20:
            clock.schedule_once(self.die, self.location.delay * rand)
            return

        # They get tired out if it's their specialty, but they go faster
        if self.specialty in (location.element1, location.element2):
            self.countdown = self.location.delay * 0.75
            self.exhaustion += 1
            clock.schedule_once(
                self.report, self.location.frequency * 0.75,
                self.countdown)
            return

        # Just your average joe, taking his good old time
        clock.schedule_once(
            self.report, self.location.frequency, self.location.delay)

    def die(self, delay):
        self.chat_pane.recv_msg(self, self.location.death_message)

    def report(self, delay, length):
        length -= delay
        if length < 0:
            self.chat_pane.recv_msg(
                self, self.location.success_message, self.location.clue)
            self.clue_pane.add_clue(self.location.clue)
        else:
            message = self.location.get_message()
            if message:
                self.chat_pane.recv_msg(self, message)
            clock.schedule_once(self.report, self.location.frequency, length)
