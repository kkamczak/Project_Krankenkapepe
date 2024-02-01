import pygame
from tools.settings import UI_ITEM_IMAGE_SIZE
from tools.support import scale_image, puts


class Item:
    items = []

    def __init__(self, item_id, name, kind, owner, price, active):
        self.item_id = item_id
        self.name = name
        self.text = 'Default'
        self.kind = kind
        self.owner = owner
        self.price = price
        self.active = active


class Sword(Item):
    def __init__(self, item_id, name, kind, owner, price, damage, active=False):
        super().__init__(item_id, name, kind, owner, price, active)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/straight_sword_1.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.text = 'Obrażenia'
        self.damage = damage


class Bow(Item):
    def __init__(self, item_id, name, kind, owner, price, damage, active=False):
        super().__init__(item_id, name, kind, owner, price, active)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/short_bow_1.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.text = 'Obrażenia'
        self.damage = damage


class Shield(Item):
    def __init__(self, item_id, name, kind, owner, price, damage, active=False):
        super().__init__(item_id, name, kind, owner, price, active)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/wooden_shield_1.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.text = 'Pancerz'
        self.damage = damage


class Potion(Item):
    def __init__(self, item_id, name, kind, owner, price, damage, active=False):
        super().__init__(item_id, name, kind, owner, price, active)

        # Load Image:
        self.image = pygame.image.load('content/graphics/items/small_health_potion.png').convert_alpha()
        self.image = scale_image(self.image, UI_ITEM_IMAGE_SIZE)
        self.rect = self.image.get_rect()

        # Properties:
        self.text = 'Punkty życia'
        self.damage = damage


def create_items(item_list: list, owner: tuple) -> list:
    """
    Creates items from a list

    :param item_list: list of items
    :param owner: owner, like player or chest
    :return: list of items as objects
    """
    items = []
    for item in item_list:
        new_id = len(Item.items)
        if item['kind'] == 'sword':
            item_x = Sword(new_id, item['name'], item['kind'], owner, item['price'], item['damage'],
                           active=True)
        elif item['kind'] == 'bow':
            item_x = Bow(new_id, item['name'], item['kind'], owner, item['price'], item['damage'], active=True)
        elif item['kind'] == 'shield':
            item_x = Shield(new_id, item['name'], item['kind'], owner, item['price'], item['damage'],
                            active=True)
        elif item['kind'] == 'item':
            item_x = Potion(new_id, item['name'], item['kind'], owner, item['price'], item['damage'],
                            active=True)
            # item_id, name, kind, owner, price, damage
        else:
            continue
        items.append(item_x)
        Item.items.append(item_x)
        puts(f'Utworzono item {item["name"]} o ID: {new_id}')
    return items
