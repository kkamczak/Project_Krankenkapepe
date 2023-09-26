level_0 = {
        'terrain': 'content/levels/0/level_0._terrain.csv',
        'terrain_elements': 'content/levels/0/level_0._terrain_elements.csv',
        'enemies': 'content/levels/0/level_0._enemies.csv',
        'player': 'content/levels/0/level_0._player.csv',
        'unlock': 1
}
level_1 = {
        'terrain': 'content/levels/1/level_1._terrain.csv',
        'terrain_elements': 'content/levels/1/level_1._terrain_elements.csv',
        'enemies': 'content/levels/1/level_1._enemies.csv',
        'player': 'content/levels/1/level_1._player.csv',
        'unlock': 1
}


levels = {
    0: level_0,
    1: level_1
}

straight_sword_1 = {
            'name': 'Prosty Miecz',
            'kind': 'sword',
            'damage': 60,
            'price': 99
        }

short_bow_1 = {
            'name': 'Krótki Łuk',
            'kind': 'bow',
            'damage': 50,
            'price': 94
        }

wooden_shield_1 = {
            'name': 'Drewniana Tarcza',
            'kind': 'shield',
            'damage': 0,
            'price': 56
        }

small_potion_1 = {
            'name': 'Mała Mikstura Leczenia',
            'kind': 'item',
            'damage': 0,
            'price': 67
        }

START_ITEMS_LIST = [
    straight_sword_1,
    short_bow_1,
    wooden_shield_1,
    small_potion_1,
    straight_sword_1,
    small_potion_1
]

chest_1 = [short_bow_1, small_potion_1]
chest_2 = []
chest_3 = [wooden_shield_1]
CHESTS_CONTENT = [chest_1, chest_2, chest_3]