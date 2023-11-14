import pygame.font
pygame.font.init()

# Sounds:
SOUND_PLAY_MUSIC = False
MUSIC_VOLUME = 0.03

# Fonts:
BIG_FONT = pygame.font.SysFont('content/fonts/arial.ttf', 72)
NORMAL_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 30)
SMALL_STATUS_FONT = pygame.font.SysFont('arial', 15)
UI_FRAME_FONT = pygame.font.SysFont('arial', 11)
UI_EQUIPMENT_ACTIVE_FONT = pygame.font.SysFont('arial', 15)
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
GREEN = (127,255,0)
BUTTON_BASIC_COLOR = (105, 77, 86)
BUTTON_ACTIVE_COLOR = (181, 11, 65)
MASK_ALPHA = 150

# Game settings:
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
TILE_SIZE = 48
PRIMAL_TILE_SIZE = 32
SCALE = TILE_SIZE / PRIMAL_TILE_SIZE

# Player settings:
PLAYER_SIZE = (30*SCALE, 57*SCALE)
PLAYER_SPEED = 4*SCALE
PLAYER_GRAVITY = 0.8*SCALE
PLAYER_JUMP_SPEED = -12*SCALE
PLAYER_MAX_HEALTH = 1000

PLAYER_ANIMATIONS_PATH = 'content/graphics/character/'
PLAYER_DEATH_ANIMATION_SPEED = 0.15*SCALE

PLAYER_ATTACK_SPEED = 0.3*SCALE
PLAYER_ATTACK_SIZE = [40*SCALE, 57*SCALE]
PLAYER_ATTACK_SPACE = 25*SCALE
PLAYER_ARCH_RANGE = 1500

PLAYER_SWORD_COOLDOWN = 300
PLAYER_SWORD_DAMAGE = 60
PLAYER_ARCH_COOLDOWN = 500
PLAYER_ARCH_DAMAGE = 60
PLAYER_SHIELD_COOLDOWN = 1000
PLAYER_IMMUNITY_FROM_HIT = 300

PLAYER_DEATH_LATENCY = 2000

# Equipment settings:
EQUIPMENT_POSITION = (SCREEN_WIDTH - SCREEN_WIDTH / 4.7, SCREEN_HEIGHT / 8)
EQUIPMENT_FRAME_SIZE = (50, 60)
EQUIPMENT_FRAME_SPACE = 5
EQUIPMENT_ROWS = 8
EQUIPMENT_COLUMNS = 6
EQUIPMENT_ALPHA = 80


EQUIPMENT_ACTIVE_FRAME_SIZE = (80, 90)
EQUIPMENT_ACTIVE_FRAME_SPACE = 10
EQUIPMENT_ACTIVE_POSITION = (EQUIPMENT_POSITION[0] - EQUIPMENT_FRAME_SPACE - EQUIPMENT_ACTIVE_FRAME_SIZE[0], SCREEN_HEIGHT / 8)

# Enemy settings:
ENEMY_ANIMATIONS_PATH = 'content/graphics/enemies/'
ENEMY_SIZE = {'sceleton': (30*SCALE, 62*SCALE), 'ninja': (30*SCALE, 57*SCALE), 'wizard': (30*SCALE, 57*SCALE), 'dark_knight': (80*SCALE, 150*SCALE)}
ENEMY_SPEED = {'sceleton': 1*SCALE, 'ninja': 1*SCALE, 'wizard': 1*SCALE, 'dark_knight': 1*SCALE}
ENEMY_GRAVITY = 0.8*SCALE
ENEMY_ANIMATION_SPEED = {'sceleton': 0.15, 'ninja': 0.15, 'wizard': 0.2, 'dark_knight': 0.15}

ENEMY_HEALTH = {'sceleton': 225, 'ninja': 120, 'wizard': 60, 'dark_knight': 420}
ENEMY_DAMAGE = {'sceleton': 60, 'ninja': 60, 'wizard': 200, 'dark_knight': 420}
ENEMY_EXPERIENCE = {'sceleton': 20, 'ninja': 20, 'wizard': 50, 'dark_knight': 420}

ENEMY_ATTACK_SIZE = {'sceleton': [60*SCALE, 80*SCALE], 'ninja': [0, 0], 'wizard': [0, 0], 'dark_knight': [45*SCALE, 100*SCALE]}
ENEMY_ATTACK_SPACE = {'sceleton': 20*SCALE, 'ninja': 5*SCALE, 'wizard': 5*SCALE, 'dark_knight': 10*SCALE}
ENEMY_TRIGGER_LENGTH = {'sceleton': 300*SCALE, 'ninja': 350*SCALE, 'wizard': 450*SCALE, 'dark_knight': 250*SCALE}
ENEMY_ATTACK_SPEED = {'sceleton': 0.25, 'ninja': 0.15, 'wizard': 0.25, 'dark_knight': 0.3}
ENEMY_ATTACK_RANGE = {'sceleton': 60*SCALE, 'ninja': 300*SCALE, 'wizard': 400*SCALE, 'dark_knight': 65*SCALE}
ENEMY_ULTIMATE_ATTACK_COOLDOWN = {'wizard': 3000, 'dark_knight': 5000}
ENEMY_IMMUNITY_FROM_HIT = 300

ENEMY_DEATH_LATENCY = 3000

BULLET_DEFAULT_SPEED = {'arrow': 10*SCALE, 'death_bullet': 5*SCALE}

# Frames Per Seconds:
FPS = 60
FPS_SHOW_POS = (60, 25)

# Buttons:
BUTTON_SIZE = (200, 40)
BUTTONS_SPACE = 40

# UI:
UI_ACTIVE_EQUIPMENT_POSITION = (int(SCREEN_WIDTH / 15), SCREEN_HEIGHT - 100)
UI_FRAME_SIZE = (80, 90)
UI_ITEM_IMAGE_SIZE = (60, 70)
UI_HP_BAR_POSITION = (20, 50)

# Terrain:
TERRAIN_PATH = 'content/graphics/terrain/terrain_tiles.png'
FIREPLACE_PATH = 'content/graphics/terrain/fireplace/'
CHEST_PATH = 'content/graphics/terrain/chest/'

# Developing:

SHOW_IMAGE_RECTANGLES = False
SHOW_COLLISION_RECTANGLES = False
SHOW_HIT_RECTANGLES = True

SHOW_PLAYER_STATUS = True
SHOW_ENEMY_STATUS = False
SHOW_STATUS_SPACE = 6