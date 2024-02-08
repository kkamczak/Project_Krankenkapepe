from tools.support import puts


class Item:
    """
    item = {
        'name': item_name,
        'kind': kind,
        'damage': item_dmg,
        'price': item_price,
        'level': item_lvl
    }

    """
    items = []

    def __init__(self, item_id, info, owner, images, active):
        self.item_id = item_id
        self.name = info['name']
        self.kind = info['kind']
        self.damage = info['damage']
        self.price = info['price']
        self.level = info['level']
        self.text = 'Default'
        self.owner = owner
        self.image = images[self.kind]
        self.rect = self.image.get_rect()
        self.active = active


class Sword(Item):
    def __init__(self, item_id, info, owner, images, active=False):
        super().__init__(item_id, info, owner, images, active)

        # Properties:
        self.text = 'Obrażenia'


class Bow(Item):
    def __init__(self, item_id, info, owner, images, active=False):
        super().__init__(item_id, info, owner, images, active)

        # Properties:
        self.text = 'Obrażenia'


class Shield(Item):
    def __init__(self, item_id, info, owner, images, active=False):
        super().__init__(item_id, info, owner, images, active)

        # Properties:
        self.text = 'Pancerz'


class Potion(Item):
    def __init__(self, item_id, info, owner, images, active=False):
        super().__init__(item_id, info, owner, images, active)

        # Properties:
        self.text = 'Punkty życia'


def create_items(level_ref, item_list: list, owner: tuple) -> list:
    """
    Creates items from a list

    :param level: reference to level
    :param item_list: list of items
    :param owner: owner, like player or chest
    :return: list of items as objects
    """
    items = []
    for item_info in item_list:
        new_id = len(Item.items)
        if item_info['kind'] == 'sword':
            item_x = Sword(new_id, item_info, owner, level_ref.images.items)
        elif item_info['kind'] == 'bow':
            item_x = Bow(new_id, item_info, owner, level_ref.images.items)
        elif item_info['kind'] == 'shield':
            item_x = Shield(new_id, item_info, owner, level_ref.images.items)
        elif item_info['kind'] == 'item':
            item_x = Potion(new_id, item_info, owner, level_ref.images.items)
        else:
            continue
        items.append(item_x)
        Item.items.append(item_x)
        puts(f'Item created: {item_info["name"]}  -  ID: {new_id}')
    return items
