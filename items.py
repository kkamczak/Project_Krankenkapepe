import pygame
from settings import UI_ITEM_IMAGE_SIZE
from support import scale_image
from game_data import START_ITEMS_LIST
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

def create_start_items() -> list:
        start_items = []
        for item_id, item in enumerate(START_ITEMS_LIST):
            #print(item[item_id]['name'])
            if item['kind'] == 'sword':
                item_x = Sword(item_id, item['name'], item['kind'], 'player', item['price'], item['damage'])
            elif item['kind'] == 'bow':
                item_x = Bow(item_id, item['name'], item['kind'], 'player', item['price'], item['damage'])
            elif item['kind'] == 'shield':
                item_x = Shield(item_id, item['name'], item['kind'], 'player', item['price'], item['damage'])
            elif item['kind'] == 'potion':
                item_x = Potion(item_id, item['name'], item['kind'], 'player', item['price'], item['damage'])
                         # item_id, name, kind, owner, price, damage
            else:
                continue
            start_items.append(item_x)
        return start_items