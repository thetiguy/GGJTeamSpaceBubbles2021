# General fonts used throughout the game
ASSET_PREFIX = 'assets/{0}'
BORDER_WIDTH = 20
CLUE_PREFIX = ASSET_PREFIX.format('clues/{0}')
# How long it takes for the monster to reach the victim in seconds. This will
# be scaled by the SPEED variable.
GAME_LENGTH = 50400
FONTS = ['Arial', 'Cantarell-Regular']  # Cantarell makes linux fonts work
MUSIC_PREFIX = ASSET_PREFIX.format('music/{0}')
PROFILE_PREFIX = ASSET_PREFIX.format('profiles/{0}')
# The speed of the game. 1 means 1 realtime. 2 means time passes twice as slow
# in game than in real life. 0.5 means time in game passes twice as fast than
# reality.
SPEED = 0.004  # Approximately 15 seconds is an hour in game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Mystery Gang'
SPRITE_SIZE = 60
# Time that's displayed is multiplied by this. This enables you to have time
# go faster in game than reality when paired with the SPEED option. If set to
# 1, the displayed time decreases in real time. If set to larger than 1, the
# displayed time decreases really fast. If less than 1 it decreases slowly.
TIME_DISPLAY_FACTOR = 248
