
class Item:
    """
    Item
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
