import pygame
from settings import UI_ITEM_IMAGE_SIZE
from support import scale_image

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
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.damage = damage

class Bow(Item):
    def __init__(self, item_id, name, kind, owner, price, damage):
        super().__init__(item_id, name, kind, owner, price)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/short_bow_1.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.damage = damage

class Shield(Item):
    def __init__(self, item_id, name, kind, owner, price, damage):
        super().__init__(item_id, name, kind, owner, price)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/wooden_shield_1.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.damage = damage

class Potion(Item):
    def __init__(self, item_id, name, kind, owner, price, damage):
        super().__init__(item_id, name, kind, owner, price)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/small_health_potion.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.damage = damage