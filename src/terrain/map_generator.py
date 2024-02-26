import random
from pygame.sprite import Group
from tools.support import import_csv_file
from tools.game_data import level_render
from tools.settings import LEVEL_SPAWN, SCREEN_WIDTH, LEVEL_SPAWN_SPACE, TILE_SIZE, LEVEL_SPAWN_HEIGHT
from entities.enemies import Sceleton, Ninja, Wizard, DarkKnight
from terrain.tiles import StaticTile, Bonfire
from terrain.chest import Chest
from terrain.portal import Portal


def generate_map() -> tuple[list, list]:
    """
    This function generate map and map elements.

    :return: tuple that contains map and elements like chest or bonfire.
    """
    level_map = ['start']
    renders = ['1', '2', '3', '4']
    for x in range(0, 4):
        level_map.append(random.choice(renders)[0])
    level_map.append('end')
    loaded_segments = {}
    loaded_elements = {}
    index = 0
    for segment in level_map:
        loaded_segments[f'{index}_{segment}'] = import_csv_file(level_render[segment])
        loaded_elements[f'{index}_{segment}'] = import_csv_file(level_render[f'{segment}_elements'])
        index += 1
    final_map = loaded_segments['0_start']
    final_map_elements = loaded_elements['0_start']
    for key, segment in loaded_segments.items():
        if key == '0_start':
            continue
        final_map = [row_final + row_segment for row_final, row_segment in zip(final_map, segment)]
    for key, segment in loaded_elements.items():
        if key == '0_start':
            continue
        final_map_elements = [row_final + row_segment for row_final, row_segment in zip(final_map_elements, segment)]
    return final_map, final_map_elements


def generate_enemies(map_length):
    spawn_point = LEVEL_SPAWN
    spawn_list = [[spawn_point]]

    while spawn_point < map_length - LEVEL_SPAWN / 2:
        amount = random.randint(1, 3)
        for multiplier in range(amount):
            spawn_list[0].append(spawn_point + multiplier * LEVEL_SPAWN_SPACE)
        spawn_point += LEVEL_SPAWN
    spawn_list[0].append(map_length - SCREEN_WIDTH / 2)
    print(spawn_list)
    return spawn_list


def generate_enemy_kind(boss: bool = False):
    if not boss:
        return random.choice(['0', '1', '2'])[0]
    else:
        return '3'


def create_tile_group(layout, kind, images, level_map, fighting):
    """
    Create a group of tiles from a layout.

    Args:
        layout (list): The layout specifying the arrangement of tiles.
        kind (str): The kind of tiles to create.

    Returns:
        pygame.sprite.Group: A group of sprite objects representing the tiles.
    """
    sprite_group = Group()
    enemy_id: int = 0
    tile_id: int = 0
    sprite: object = None

    for row_index, row in enumerate(layout):
        for col_index, val in enumerate(row):
            if val != str(-1):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if kind == 'terrain':
                    if int(val) == 11:
                        tile_surface = images.terrain_tiles[int(val)]
                        sprite = StaticTile(tile_id, TILE_SIZE, x, y, tile_surface)
                        tile_id += 1

                elif kind == 'collideable':
                    if int(val) != 11:
                        tile_surface = images.terrain_tiles[int(val)]
                        sprite = StaticTile(tile_id, TILE_SIZE, x, y, tile_surface)
                        tile_id += 1
                elif kind == 'terrain_elements':
                    if val == '0':
                        sprite = Chest(tile_id, TILE_SIZE, x, y, images.terrain_elements['chest'], level_map)
                        tile_id += 1
                    elif val == '1':
                        sprite = Bonfire(tile_id, TILE_SIZE, x, y, images.terrain_elements['bonfire'])
                        tile_id += 1
                    elif val == '2':
                        sprite = Portal(tile_id, TILE_SIZE, (x, y), images.terrain_elements['portal'])
                        tile_id += 1

                elif kind == 'enemies':
                    pos = (int(val), LEVEL_SPAWN_HEIGHT)
                    if col_index < len(layout[0]) - 1:
                        value = generate_enemy_kind()
                    else:
                        value = generate_enemy_kind(boss=True)
                    if value == '0':
                        sprite = Sceleton(
                            level_map.current_level,
                            enemy_id,
                            pos,
                            (images.enemies[0]['sceleton'], images.enemies[1]['sceleton']),
                            fighting.sword_attack
                        )
                        enemy_id += 1
                    elif value == '1':
                        sprite = Ninja(
                            level_map.current_level,
                            enemy_id,
                            pos,
                            (images.enemies[0]['ninja'], images.enemies[1]['ninja']),
                            fighting.arch_attack
                        )
                        enemy_id += 1
                    elif value == '2':
                        sprite = Wizard(
                            level_map.current_level,
                            enemy_id,
                            pos,
                            (images.enemies[0]['wizard'], images.enemies[1]['wizard']),
                            fighting.arch_attack,
                            fighting.thunder_attack
                        )
                        enemy_id += 1
                    elif value == '3':
                        sprite = DarkKnight(
                            level_map.current_level,
                            enemy_id,
                            pos,
                            (images.enemies[0]['dark_knight'], images.enemies[1]['dark_knight']),
                            fighting.sword_attack
                        )
                        enemy_id += 1
                if sprite is not None:
                    sprite_group.add(sprite)
    return sprite_group

