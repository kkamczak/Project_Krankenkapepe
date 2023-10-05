"""
This module defines various tile classes for use in a 2D game.

It includes static, animated, and chest tiles, as well as functions to check for usable elements
and create item content for chests.

Classes:
    - Tile: A base class for all types of tiles.
    - StaticTile: Represents a static, non-animated tile.
    - AnimatedTile: Represents an animated tile with multiple frames.
    - Chest: Represents a chest tile that can contain items.

Functions:
    - check_for_usable_elements(character, elements): Checks for usable elements near the character.
"""
import pygame
from support import import_folder, puts
from game_data import CHESTS_CONTENT
from items import create_items

class Tile(pygame.sprite.Sprite):
    """
    Initialize a Tile object.

    Args:
        id (int): The unique identifier for the tile.
        size (tuple[int, int]): The size of the tile (width, height).
        x (int): The x-coordinate of the tile's top-left corner.
        y (int): The y-coordinate of the tile's top-left corner.
    """
    def __init__(self, tile_id: int, size: int, x_pos: int, y_pos: int) -> None:
        super().__init__()
        self.kind = 'terrain'
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))
        self.id = tile_id

    def draw(self, surface: pygame.Surface, offset: pygame.math.Vector2) -> None:
        """
        Draw the tile on the given surface with the specified offset.

        Args:
            surface (pygame.Surface): The surface to draw the tile on.
            offset (pygame.math.Vector2): The offset to apply to the tile's position.
        """
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class StaticTile(Tile):
    """
    Initialize a StaticTile object.

    Args:
        id (int): The unique identifier for the tile.
        size (tuple[int, int]): The size of the tile (width, height).
        x (int): The x-coordinate of the tile's top-left corner.
        y (int): The y-coordinate of the tile's top-left corner.
        surface (pygame.Surface): The surface representing the static tile.
    """
    def __init__(self, tile_id: int, size: tuple[int, int],
                 x_pos: int, y_pos: int, surface: pygame.Surface) -> None:
        super().__init__(tile_id, size, x_pos, y_pos)
        self.image = surface

class AnimatedTile(Tile):
    """
    Initialize an AnimatedTile object.

    Args:
        id (int): The unique identifier for the tile.
        size (tuple[int, int]): The size of the tile (width, height).
        x (int): The x-coordinate of the tile's top-left corner.
        y (int): The y-coordinate of the tile's top-left corner.
        path (str): The path to the folder containing animation frames.
    """
    def __init__(self, tile_id: int, size: tuple[int, int],
                 x_pos: int, y_pos: int, path: str) -> None:
        super().__init__(tile_id, size, x_pos, y_pos)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.usable = False

    def animate(self) -> None:
        """Animate the tile by cycling through its frames."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        """Update the animated tile by advancing its animation frames."""
        self.animate()

class Chest(AnimatedTile):
    """
    Represents a chest tile in the game.

    Chests can contain items and are animated. Players can interact with chests to collect their content.

    Attributes:
        chests (list[Chest]): A list to keep track of all created chest instances.

    Args:
        id (int): The unique identifier for the chest.
        size (tuple[int, int]): The size of the chest (width, height).
        x (int): The x-coordinate of the chest's top-left corner.
        y (int): The y-coordinate of the chest's top-left corner.
        path (str): The path to the folder containing animation frames for the chest.

    Methods:
        animate_once: Animate the chest once and mark it as animated.
        create_content: Create the content (items) for the chest.
        action: Perform an action on the chest (collect its content).
        update: Update the chest's animation frame.
    """
    chests = []
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int, path: str) -> None:
        """
        Initialize a Chest object.

        Args:
            id (int): The unique identifier for the chest.
            size (tuple[int, int]): The size of the chest (width, height).
            x (int): The x-coordinate of the chest's top-left corner.
            y (int): The y-coordinate of the chest's top-left corner.
            path (str): The path to the folder containing animation frames for the chest.
        """
        super().__init__(id, size, x, y, path)
        self.kind = 'chest'
        self.collected = False
        self.animated = False
        self.usable = True
        self.content = self.create_content()
        puts(f'Stworzono skrzynie, id {self.id}')
        Chest.chests.append(self)
    def animate_once(self) -> None:
        """Animate the chest once, then mark it as animated."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
            self.animated = True
        self.image = self.frames[int(self.frame_index)]
    def create_content(self) -> list:
        """Create the content (items) for the chest."""
        content = []
        Chest.chests = []

        puts(str(len(Chest.chests)))
        for element in create_items(CHESTS_CONTENT[len(Chest.chests)]):
            content.append(element)
        return content
    def action(self) -> list:
        """Perform an action on the chest (collect its content)."""
        return self.content
    def update(self):
        if self.collected and not self.animated:
            self.animate_once()

def check_for_usable_elements(character, elements) -> list:
    """
    Check for usable elements (e.g., chests) near the character.

    Args:
        character: The character to check proximity to.
        elements: The list of elements to check for usability.

    Returns:
        list: A list containing a boolean indicating
        if a usable element is found and the element itself.
    """
    for element in elements:
        if not element.usable:
            continue
        if abs(character.animations.rect.centerx - element.rect.centerx) < 50 and \
            abs(character.animations.rect.centery - element.rect.centery) < 50 and \
            not element.collected:
            return [True, element]
    return [False, None]


