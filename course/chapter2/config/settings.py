from  pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Window size
WIDTH = 630 # px
HEIGHT = 480 # px

VELOCITY = 2 # px

# frame rate
FPS = 30 # Frames per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sprites
BACKGROUND = str(BASE_DIR / 'images' / 'background.jpg')
MUSHROOM = str(BASE_DIR / 'images' / 'mushroom.png')
