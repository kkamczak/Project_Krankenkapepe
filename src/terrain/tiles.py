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
from tools.support import import_folder


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
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.id = tile_id
        self.pickable = False

    def show_pickable(self):

        image = self.image.copy()
        glow_color = (255, 165, 0)
        alpha = 180

        glow_surface = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
        glow_surface.fill((glow_color[0], glow_color[1], glow_color[2], alpha))

        image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return image

    def draw(self, surface: pygame.Surface, offset: pygame.math.Vector2) -> None:
        """
        Draw the tile on the given surface with the specified offset.

        Args:
            surface (pygame.Surface): The surface to draw the tile on.
            offset (pygame.math.Vector2): The offset to apply to the tile's position.
        """
        pos = self.rect.topleft - offset
        if self.pickable:
            surface.blit(self.show_pickable(), pos)
        else:
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
    def __init__(self, tile_id: int, size: int,
                 x_pos: int, y_pos: int, surface: pygame.Surface = None) -> None:
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
                 x_pos: int, y_pos: int, images: list) -> None:
        super().__init__(tile_id, size, x_pos, y_pos)
        self.frames = images
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self) -> None:
        """Animate the tile by cycling through its frames."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        """Update the animated tile by advancing its animation frames."""
        self.animate()


class Bonfire(AnimatedTile):
    def __init__(self, tile_id: int, size: tuple[int, int], x: int, y: int, images: list):
        super().__init__(tile_id, size, x, y, images)
        self.kind = 'bonfire'
        self.equipment = TileEquipment()


class TileEquipment:
    """
    This is class for Tile Equipment
    """
    def __init__(self, usable: bool = False) -> None:
        self.collected = False
        self.usable = usable
        self.content = None

    def add_item(self, new_item) -> None:
        for item in self.content:
            if item is new_item:
                return
        self.content.append(new_item)

    def delete_item(self, item) -> None:
        for item_owned in self.content:
            if item is item_owned:
                self.content.remove(item_owned)
                break


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
    current_usable = character.status.can_use_object[1]
    new_usable = []

    def is_close(current) -> bool:
        if abs(character.animations.rect.centerx - current.rect.centerx) < 50 and \
            abs(character.animations.rect.centery - current.rect.centery) < 50 and \
            not current.equipment.collected:
            return True
        return False
    if current_usable is not None:
        for element in current_usable:
            if is_close(element):
                new_usable.append(element)
    for element in elements:
        if not element.equipment.usable:
            continue
        element.pickable = False
        if element in new_usable:
            continue
        if abs(character.animations.rect.centerx - element.rect.centerx) < 50 and \
            abs(character.animations.rect.centery - element.rect.centery) < 50 and \
            not element.equipment.collected:
            new_usable.append(element)
    if len(new_usable) > 0:
        return [True, new_usable]
    return [False, None]


def change_loot_priority(elements_list) -> None:
    if len(elements_list) > 0:
        place_holder = elements_list[0]
        for index, element in enumerate(elements_list):
            element.pickable = False
            if index+1 < len(elements_list):
                elements_list[index] = elements_list[index+1]
            else:
                elements_list[index] = place_holder
        elements_list[0].pickable = True

