import pygame
from csv import reader
from os import walk
from settings import TILE_SIZE

def import_csv_file(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surf)

    return cut_tiles

def import_character_assets(animations, path):  # Import all animations:
    character_path = path

    for animation in animations.keys():
        full_path = character_path + animation
        animations[animation] = import_folder(full_path)

    return animations

def import_folder(path):
    surface_list = []

    for _, dirs, image_files in walk(path):
        for image in sorted(image_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def create_bar(size, color):
    max = pygame.Surface(size)
    max.fill(color)
    return max

# Drawing function:
def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))