import pygame

class Item:
    def __init__(self, item_id, name, kind, owner, price):
        self.item_id = item_id
        self.name = name
        self.kind = kind
        self.owner = owner
        self.price = price


class Sword(Item):
    def __init__(self, item_id, name, kind, owner, price, damage):
        super().__init__(item_id, name, kind, owner, price)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/straight_sword_1.png').convert_alpha()
        self.rect = self.image.get_rect()

        # Properties:
        self.damage = damage