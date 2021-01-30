#!/usr/bin/env python
import arcade

from MysteryGang.windows import MysteryGangWindow

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "wooooo"


def main():
    """Main method"""
    window = MysteryGangWindow(
        SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    window.init_game()
    arcade.run()

if __name__ == "__main__":
    main()
