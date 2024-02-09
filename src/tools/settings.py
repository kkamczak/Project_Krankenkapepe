import pygame.font
from tools.game_data import SWORD_NAMES, BOW_NAMES, ARMOR_NAMES
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
PLAYER_SPEED = 8*SCALE
PLAYER_GRAVITY = 0.8*SCALE
PLAYER_JUMP_SPEED = -12*SCALE
PLAYER_MAX_HEALTH = 2000

PLAYER_SPAWN_POSITION = (400, 300)
PLAYER_ANIMATIONS_PATH = 'content/graphics/character/'
PLAYER_DEATH_ANIMATION_SPEED = 0.15*SCALE


PLAYER_ATTACK_SIZE = [40*SCALE, 57*SCALE]
PLAYER_ATTACK_SPACE = 25*SCALE
PLAYER_ARCH_RANGE = 300

PLAYER_SWORD_SPEED = 200
PLAYER_SWORD_COOLDOWN = 1000
PLAYER_SWORD_HIT_TIME = 0.65
PLAYER_SWORD_DAMAGE = 60
PLAYER_ARCH_SPEED = 500
PLAYER_ARCH_COOLDOWN = 1000
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
EQUIPMENT_ALPHA = 190
EQUIPMENT_INFO_SIZE = (130, 140)
EQUIPMENT_INFO_ALPHA = 255

EQUIPMENT_SHOW_IDS = True

EQUIPMENT_ACTIVE_FRAME_SIZE = (80, 90)
EQUIPMENT_ACTIVE_FRAME_SPACE = 10
EQUIPMENT_ACTIVE_POSITION = (EQUIPMENT_POSITION[0] - EQUIPMENT_FRAME_SPACE - EQUIPMENT_ACTIVE_FRAME_SIZE[0], SCREEN_HEIGHT / 8)

# Loot settings:
LOOT_INDEX = 100
LOOT_WIN_SIZE = (8, 3)
LOOT_FRAME_SIZE = (30, 40)
LOOT_WIN_POS = (SCREEN_WIDTH - SCREEN_WIDTH / 4.7, SCREEN_HEIGHT / 1.3)
LOOT_KIND = 'regular'
LOOT_SPACE = 5
LOOT_HEADER_POS = (SCREEN_WIDTH - SCREEN_WIDTH / 4.7, SCREEN_HEIGHT / 1.41)

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

ENEMY_DEATH_LATENCY = 700

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
UI_SKELETON_POINTS_SPACE = (120, 50)

# Terrain:
TERRAIN_PATH = 'content/graphics/terrain/terrain_tiles.png'
FIREPLACE_PATH = 'content/graphics/terrain/fireplace/'
CHEST_PATH = 'content/graphics/terrain/chest/'
PORTAL_PATH = 'content/graphics/terrain/portal/'

# Items:
ITEM_LEVEL_WEIGHT = [0.6, 0.25, 0.15]
ITEM_DMG_MULTIPLIERS = [1.0, 5.0, 0.1]
ITEM_BASE_DMG = {
    'sword': 60,
    'bow': 90,
    'shield': 50,
    'item': 120
}
ITEM_BASE_PRICE = {
    'sword': 99,
    'bow': 76,
    'shield': 67,
    'item': 32
}
ITEM_NAMES = {
    'sword': SWORD_NAMES,
    'bow': BOW_NAMES,
    'shield': ARMOR_NAMES,
    'item': ['Potion']
}
ITEM_LOOT_ODDS_1 = {
    0: 0.5,
    1: 0.3,
    2: 0.1,
    3: 0.05,
    4: 0.03,
    5: 0.015,
    6: 0.005
}
ITEM_LOOT_ODDS_2 = {
    'sword': 0.2,
    'bow': 0.15,
    'shield': 0.15,
    'item': 0.5
}

ITEM_PATH = {
    'sword': 'content/graphics/items/straight_sword_1.png',
    'bow': 'content/graphics/items/short_bow_1.png',
    'shield': 'content/graphics/items/wooden_shield_1.png',
    'item': 'content/graphics/items/small_health_potion.png'
}
ITEM_IMAGES = {}
# Level:

LEVEL_AREA_DISTANCE = 3000
LEVEL_SPAWN = 1500
LEVEL_SPAWN_HEIGHT = 300
LEVEL_SPAWN_SPACE = 400

# Keyboard:
KEY_CD = {
    'v': 400
}

# Developing:

SHOW_IMAGE_RECTANGLES = False
SHOW_COLLISION_RECTANGLES = False
SHOW_HIT_RECTANGLES = False

SHOW_PLAYER_STATUS = False
SHOW_ENEMY_STATUS = True
SHOW_STATUS_SPACE = 6
