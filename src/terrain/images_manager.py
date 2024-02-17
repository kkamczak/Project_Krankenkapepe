import pygame
from tools.support import import_image, scale_image, import_cut_graphics, import_folder, import_character_assets
from tools.settings import TERRAIN_PATH, PRIMAL_TILE_SIZE, TILE_SIZE, CHEST_PATH, FIREPLACE_PATH, \
    SCALE, ENEMY_ANIMATIONS_PATH, ITEM_PATH, UI_ITEM_IMAGE_SIZE, PORTAL_PATH, CORPSE_PATH


class ImagesManager:
    """
    This class is used to store and manage all the images in the game
    """
    def __init__(self, screen):
        self.display_surface = screen
        self.background = self.load_background(self.display_surface.get_size(), 'content/graphics/overworld/background.png')
        self.terrain_tiles = self.load_terrain()
        self.terrain_elements = self.load_terrain_elements()
        self.enemies = self.load_enemies_animations()
        self.items = self.load_items()

    @staticmethod
    def load_background(size, path) -> pygame.surface.Surface:
        """
        This method loads background

        :return: background image
        """
        background = import_image(path)
        background = scale_image(background, size)
        return background

    @staticmethod
    def load_terrain() -> list:
        """
        This method loads terrain tiles

        :return: list of images
        """
        terrain_tiles = import_cut_graphics(TERRAIN_PATH, (PRIMAL_TILE_SIZE, PRIMAL_TILE_SIZE))
        scaled_tiles = []
        for tile in terrain_tiles:
            scaled = scale_image(tile, (TILE_SIZE, TILE_SIZE))
            scaled_tiles.append(scaled)
        return scaled_tiles

    @staticmethod
    def load_terrain_elements() -> dict:
        """
        This method loads terrain elements tiles

        :return: Returns a dictionary containing lists of images
        """
        images = {
            'bonfire': import_folder(FIREPLACE_PATH),
            'chest': import_folder(CHEST_PATH),
            'portal': import_folder(PORTAL_PATH),
            'corpse': import_image(CORPSE_PATH)
        }
        return images

    @staticmethod
    def load_enemies_animations() -> tuple[dict, dict]:
        """
        This method loads enemies animation frames.

        :return: Returns a two dictionary containing dictionary of animations and flipped animations.
        """
        enemies = {'sceleton': (SCALE*1.0, False), 'ninja': (SCALE*1.0, False), 'wizard': (SCALE*1.0, False), 'dark_knight': (SCALE*0.2, True)}
        positions = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [], 'stun': []}
        animations = {'sceleton': positions.copy(), 'ninja': positions.copy(), 'wizard': positions.copy(), 'dark_knight': positions.copy()}
        flip_animations = {'sceleton': positions.copy(), 'ninja': positions.copy(), 'wizard': positions.copy(), 'dark_knight': positions.copy()}
        for enemy, frames in animations.items():
            import_character_assets(frames, f'{ENEMY_ANIMATIONS_PATH}/{enemy}/', scale=enemies[enemy][0], flip=enemies[enemy][1])
        enemies = {'sceleton': (SCALE*1.0, True), 'ninja': (SCALE*1.0, True), 'wizard': (SCALE*1.0, True), 'dark_knight': (SCALE*0.2, False)}
        for enemy, frames in flip_animations.items():
            import_character_assets(frames, f'{ENEMY_ANIMATIONS_PATH}/{enemy}/', scale=enemies[enemy][0], flip=enemies[enemy][1])
        return animations, flip_animations

    @staticmethod
    def load_items() -> dict:
        """
        This method loads items images.

        :return: Returns a dictionary containing item images.
        """
        items = {}
        for item, path in ITEM_PATH.items():
            items[item] = pygame.image.load(path).convert_alpha()
            items[item] = scale_image(items[item], UI_ITEM_IMAGE_SIZE)
        return items
