import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MysteryGangWindow(arcade.Window):
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.F11:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""
        super().on_resize(width, height)

    def on_show(self):
        """This is run once when we switch to this view."""
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
