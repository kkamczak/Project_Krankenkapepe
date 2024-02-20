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
level_render = {
    'start': 'content/levels/1/render_start_terrain.csv',
    'start_elements': 'content/levels/1/render_start_terrain_elements.csv',
    '1': 'content/levels/1/render_1_terrain.csv',
    '1_elements': 'content/levels/1/render_1_terrain_elements.csv',
    '2': 'content/levels/1/render_2_terrain.csv',
    '2_elements': 'content/levels/1/render_2_terrain_elements.csv',
    '3': 'content/levels/1/render_3_terrain.csv',
    '3_elements': 'content/levels/1/render_3_terrain_elements.csv',
    '4': 'content/levels/1/render_4_terrain.csv',
    '4_elements': 'content/levels/1/render_4_terrain_elements.csv',
    'end': 'content/levels/1/render_end_terrain.csv',
    'end_elements': 'content/levels/1/render_end_terrain_elements.csv',
}


levels = {
    0: level_0,
    1: level_1
}

straight_sword_1 = {
            'name': 'Prosty Miecz',
            'kind': 'sword',
            'damage': 60,
            'price': 99,
            'level': 1
        }

short_bow_1 = {
            'name': 'Krótki Łuk',
            'kind': 'bow',
            'damage': 50,
            'price': 94,
            'level': 1
        }

wooden_shield_1 = {
            'name': 'Drewniana Tarcza',
            'kind': 'shield',
            'damage': 12,
            'price': 56,
            'level': 1
        }

small_potion_1 = {
            'name': 'Mikstura Leczenia',
            'kind': 'item',
            'damage': 120,
            'price': 67,
            'level': 1
        }

SWORD_NAMES = [
    "Ostrze Kruka",
    "Smocza Łza",
    "Miecz Nocy",
    "Krwawa Ostrzałka",
    "Płomienne Ostrze",
    "Miecz Mrozu",
    "Błyskawiczny Miecz",
    "Koronny Rozpruwacz",
    "Szkarłatny Katana",
    "Miecz Słowian",
    "Długi Cios",
    "Złoty Ostróg",
    "Ostrze Gryfa",
    "Kryształowy Kord",
    "Żelazny Skrytobójca",
    "Miecz Zaklętych Ciemności",
    "Czysty Miecz",
    "Diamentowy Rozdział",
    "Elfia Zbroja",
    "Skorpiony Nóż",
    "Płetwiczka",
    "Perłowy Miecz",
    "Strzała Wiatru",
    "Dębowa Kosa",
    "Kamienny Wrzask"
]

BOW_NAMES = [
    "Łuk Mistrza Strzału",
    "Kusza Elfów",
    "Łuk Księżycowy",
    "Wiatrówka",
    "Strzały Cienia",
    "Łuk Kryształowy",
    "Łuk Smoka",
    "Elfia Rozpacz",
    "Łuk Niebios",
    "Łuk Półksiężyca",
    "Łuk Przeznaczenia",
    "Strzały Mrozu",
    "Łuk Gromu",
    "Łuk Skrytobójcy",
    "Łuk Nocy",
    "Łuk Lśniących Gwiazd",
    "Łuk Kowala",
    "Łuk Zeładowany",
    "Strzały Słoneczne",
    "Łuk Cieni",
    "Łuk Zaklęty",
    "Łuk Różany",
    "Łuk Łowcy",
    "Łuk Żywiołów",
    "Strzała Świtu"
]

ARMOR_NAMES = [
    "Zbroja Bojownika",
    "Płaszcz Niewidki",
    "Pancerz Krasnoluda",
    "Zbroja Maga",
    "Zbroja Łotrzyka",
    "Nagolenniki Zdobywcy",
    "Zbroja Kryształowa",
    "Płaszcz Nocnego Łowcy",
    "Pancerz Słoneczny",
    "Zbroja Strażnika",
    "Płaszcz Niewidzialności",
    "Nagolenniki Mrocznego Rycerza",
    "Zbroja Słonecznego Wędrowca",
    "Zbroja Złodzieja",
    "Pancerz Smoczy",
    "Zbroja Zaklinacza",
    "Zbroja Cienia",
    "Pancerz Wojownika Światła",
    "Płaszcz Szybkości",
    "Nagolenniki Zaklęte",
    "Zbroja Mrocznego Elfika",
    "Zbroja Ognistej Furii",
    "Pancerz Zamarzającego Serca",
    "Płaszcz Pająka",
    "Zbroja Szermierza"
]

START_ITEMS_LIST = [
    straight_sword_1,
    short_bow_1,
    wooden_shield_1,
    small_potion_1,
    straight_sword_1,
    small_potion_1
]

chest_1 = [short_bow_1, small_potion_1]
chest_2 = [straight_sword_1]
chest_3 = [wooden_shield_1]
CHESTS_CONTENT = [chest_1, chest_2, chest_3, chest_1, chest_2, chest_3, chest_1, chest_2, chest_3]
CORPSE_CONTENT = [chest_1, chest_2, chest_3, chest_1, chest_2, chest_3, chest_1, chest_2, chest_3]
