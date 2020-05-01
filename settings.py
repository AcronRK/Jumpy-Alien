# this file contains options, constants and settings of the game
TITLE = "AlienScape"
WIDTH = 480
HEIGHT = 600
FPS = 60
MOVING_SCREEN = 1
FONT_NAME = "comicsans"
SPRITESHEET = "spritesheet_jumper.png"

# Player propreties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_SPRITESHEET = "p1_spritesheet.png"

# Projectile propreties
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 30
PROJECTILE_SPEED = 8

# platforms
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (148, 0, 211)

