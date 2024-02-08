import pygame
from tools.support import import_image, puts
from entities.enemies import Enemy
from terrain.tiles import StaticTile, TileEquipment
from terrain.items_generator import generate_content_amount, generate_loot_content


class Corpse(StaticTile):
    """
    Class for corpse created after defeating enemy.
    """
    def __init__(self, level_ref, tile_id: int, level: int, size: int, x_pos: int, y_pos: int, amount: int) -> None:
        super().__init__(tile_id, size, x_pos, y_pos)
        image = import_image('content/graphics/terrain/corpse/1.png')
        self.kind = 'corpse'
        self.level = level
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
        self.equipment = TileEquipment(True)
        self.create_content(level_ref, amount)

    def create_content(self, level_ref, amount) -> None:
        self.equipment.content = generate_loot_content(level_ref, amount, (self, self.kind))
        puts(f'Generated content for corpse id={self.id}')

    def update(self):
        super(Corpse, self).update()
        if len(self.equipment.content) < 1 and not self.pickable:
            puts('Koniec puste usuwam')
            self.equipment.collected = True
            self.kill()


def create_corpse(level_ref, enemy: Enemy, group: pygame.sprite.Group) -> None:
    """
    This function creates a corpse object based on a dead enemy

    :param level_ref: reference to map level object
    :param enemy: dead enemy
    :param group: group containing terrain elements
    :return: none
    """
    amount = generate_content_amount()
    if amount > 0:
        corpse = Corpse(
            level_ref,
            enemy.status.id,
            enemy.properties.level,
            32,
            enemy.animations.rect.midbottom[0],
            enemy.animations.rect.midbottom[1],
            amount
        )
        group.add(corpse)
    else:
        puts('Wylosowano 0 przedmiotów, usuwam zwłoki')
