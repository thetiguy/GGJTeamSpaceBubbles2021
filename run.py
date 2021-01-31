#!/usr/bin/env python
import arcade

from MysteryGang.windows import MysteryGangWindow
from MysteryGang.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """Main method"""
    MysteryGangWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                      resizable=True)
    arcade.run()


if __name__ == "__main__":
    main()
