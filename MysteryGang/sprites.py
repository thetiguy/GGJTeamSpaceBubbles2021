import arcade

from .constants import PROFILE_PREFIX


class LocationSprite(arcade.SpriteSolidColor):
    """Location sprite object, used to assign investigators."""

    def __init__(self, location, w, h, color=None):
        self.location = location
        if color is None:
            color = arcade.color.GRAY
        super().__init__(w, h, color)


class WorkerSprite(arcade.Sprite):
    """investiator sprite object."""

    locked = False

    def __init__(self, worker, scale, center_x, center_y):
        self.worker = worker
        self.start_x = center_x
        self.start_y = center_y
        path = PROFILE_PREFIX.format('{0}.png'.format(worker.name))
        super().__init__(path, scale, center_x=center_x, center_y=center_y)
