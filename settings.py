import pygame.font
pygame.font.init()

# Fonts:
NORMAL_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 30)
SMALL_STATUS_FONT = pygame.font.SysFont('arial', 15)
UI_FRAME_FONT = pygame.font.SysFont('arial', 11)
DEATH_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 70)
FPS_FONT = pygame.font.SysFont('arial', 30)
BUTTON_FONT = pygame.font.SysFont('arial', 25)

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (219, 216, 206)
RED = (181, 11, 65)
SKY = (12, 64, 94)
YELLOW = (224, 187, 123)
BUTTON_BASIC_COLOR = (105, 77, 86)
BUTTON_ACTIVE_COLOR = (181, 11, 65)

# Game settings:
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
RESOLUTION_SCALE = 2
TILE_SIZE = 32

# Player settings:
PLAYER_SIZE = (30, 57)
PLAYER_SPEED = 4
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_SPEED = -12
PLAYER_MAX_HEALTH = 1500

PLAYER_ANIMATIONS_PATH = 'content/graphics/character/'
PLAYER_DEATH_ANIMATION_SPEED = 0.15

PLAYER_ATTACK_SPEED = 0.3
PLAYER_ATTACK_SIZE = [40, 57]
PLAYER_ATTACK_SPACE = 25

SWORD_ATTACKING_COOLDOWN = 1000
SHIELD_COOLDOWN = 1000
IMMUNITY_FROM_HIT = 300

# Enemy settings:
ENEMY_ANIMATIONS_PATH = 'content/graphics/enemies/'
ENEMY_SIZE = {'sceleton': (30, 62), 'ninja': (30, 57), 'wizard': (30, 57), 'dark_knight': (80, 150)}
ENEMY_SPEED = {'sceleton': 1, 'ninja': 1, 'wizard': 1, 'dark_knight': 1}
ENEMY_GRAVITY = 0.8
ENEMY_ANIMATION_SPEED = {'sceleton': 0.15, 'ninja': 0.15, 'wizard': 0.2, 'dark_knight': 0.15}

ENEMY_HEALTH = {'sceleton': 225, 'ninja': 120, 'wizard': 60, 'dark_knight': 420}
ENEMY_DAMAGE = {'sceleton': 60, 'ninja': 60, 'wizard': 200, 'dark_knight': 420}
ENEMY_EXPERIENCE = {'sceleton': 20, 'ninja': 20, 'wizard': 50, 'dark_knight': 420}

ENEMY_ATTACK_SIZE = {'sceleton': [60, 60], 'dark_knight': [50, 150]}
ENEMY_ATTACK_SPACE = {'sceleton': 20, 'ninja': 5, 'wizard': 5, 'dark_knight': 40}
ENEMY_TRIGGER_LENGTH = {'sceleton': 300, 'ninja': 350, 'wizard': 450, 'dark_knight': 250}
ENEMY_ATTACK_SPEED = {'sceleton': 0.25, 'ninja': 0.15, 'wizard': 0.25, 'dark_knight': 0.15}
ENEMY_ATTACK_RANGE = {'sceleton': 80, 'ninja': 300, 'wizard': 400, 'dark_knight': 60}
ENEMY_ULTIMATE_ATTACK_COOLDOWN = {'wizard': 3000, 'dark_knight': 5000}

BULLET_DEFAULT_SPEED = {'arrow': 10, 'death_bullet': 5}

# Frames Per Seconds:
FPS = 60
FPS_SHOW_POS = (60, 25)

# Buttons:
BUTTON_SIZE = (200, 40)
BUTTONS_SPACE = 40

# UI:
UI_ACTIVE_EQUIPMENT_POSITION = (SCREEN_WIDTH / 15, SCREEN_HEIGHT - 100)
UI_FRAME_SIZE = (80, 90)
UI_ITEM_IMAGE_SIZE = (60, 70)
UI_HP_BAR_POSITION = (20, 50)

# Developing:

SHOW_IMAGE_RECTANGLES = False
SHOW_COLLISION_RECTANGLES = True
SHOW_HIT_RECTANGLES = True

SHOW_PLAYER_STATUS = True
SHOW_ENEMY_STATUS = True
SHOW_STATUS_SPACE = 6