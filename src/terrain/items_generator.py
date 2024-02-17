import random
from tools.settings import ITEM_LEVEL_WEIGHT, ITEM_DMG_MULTIPLIERS, ITEM_BASE_DMG, ITEM_BASE_PRICE, \
    ITEM_NAMES, ITEM_LOOT_ODDS_1, ITEM_LOOT_ODDS_2
from terrain.items import Item, Sword, Bow, Shield, Potion


def generate_content_amount() -> int:
    """
    This function generates the number of items in chest or hat have fallen off the opponent

    :return: amount of items
    """
    weights = []
    amounts = []
    for key, value in ITEM_LOOT_ODDS_1.items():
        amounts.append(key)
        weights.append(value)
    amount = random.choices(amounts, weights=weights)[0]  # How many items dropped
    return amount


def generate_item(level: int, kind: str) -> dict:
    """
    Generating dictionary with parameters for new item

    :return: dict with parameters
    """
    levels = [level, level+1, level+2]
    item_lvl = random.choices(levels, weights=ITEM_LEVEL_WEIGHT)[0]  # What item dropped
    start = ITEM_DMG_MULTIPLIERS[0]
    end = ITEM_DMG_MULTIPLIERS[1]
    step = ITEM_DMG_MULTIPLIERS[2]
    multipliers = [round(x, 1) for x in [start + i * step for i in range(int((end - start) / step) + 1)]]
    multiplier = random.choices(multipliers)[0]
    item_dmg = int(ITEM_BASE_DMG[kind] + item_lvl * multiplier)
    item_price = int(ITEM_BASE_PRICE[kind] + item_lvl * multiplier)
    item_name = random.choices(ITEM_NAMES[kind])[0]
    item = {
        'name': item_name,
        'kind': kind,
        'damage': item_dmg,
        'price': item_price,
        'level': item_lvl
    }
    return item


def generate_loot_content(level, amount: int, owner: list) -> list:
    """
    This function generates items that will be placed in the corpse
    :param level: reference to map level
    :param amount: items amount
    :param owner: corpse for which a list is generated [object, 'kind of object']
    :return: list of items
    """
    items_generated = []
    for place in range(0, amount):
        weights = []
        items = []
        for key, value in ITEM_LOOT_ODDS_2.items():
            items.append(key)
            weights.append(value)
        item_kind = random.choices(items, weights=weights)[0]  # What item dropped
        items_generated.append(generate_item(owner[0].level, item_kind))
    content = []
    for element in create_items(level, items_generated, owner):
        content.append(element)
    return content


def create_items(level_ref, item_list: list, owner: list) -> list:
    """
    Creates items from a list

    :param level_ref: reference to map level
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
    return items


def clean_items(item_list) -> None:
    """
    This functions removes items, if it doesn't belong to player.

    :param item_list: list of all items
    :return: None
    """
    counter = 0
    items_to_remove = []
    for item in item_list:
        if item.owner[1] != 'player':
            items_to_remove.append(item)
            counter += 1
    for item in items_to_remove:
        item_list.remove(item)
        del item
