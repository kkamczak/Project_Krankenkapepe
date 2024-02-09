import random
from tools.support import import_csv_file
from tools.game_data import level_render
from tools.settings import LEVEL_SPAWN, SCREEN_WIDTH, LEVEL_SPAWN_SPACE


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

