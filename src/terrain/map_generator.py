import random
from tools.support import import_csv_file
from tools.game_data import level_render


def generate_map() -> tuple[list, list]:
    """
    This function generate map and map elements.

    :return: tuple that contains map and elements like chest or bonfire.
    """
    level_map = ['start']
    renders = ['1', '2', '3', '4']
    for x in range(0, 30):
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




