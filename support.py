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

def import_cut_graphics(path: str, size: tuple[int, int]) -> list:
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / size[0])
    tile_num_y = int(surface.get_size()[1] / size[1])

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size[0]
            y = row * size[1]
            new_surf = pygame.Surface(size, flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size[0], size[1]))
            cut_tiles.append(new_surf)

    return cut_tiles

def import_character_assets(animations, path, scale: float = 1.0, flip: bool = False):  # Import all animations:
    character_path = path

    for animation in animations.keys():
        full_path = character_path + animation
        animations[animation] = import_folder(full_path, scale, flip)

    return animations

def import_folder(path: str, scale: float = 1.0, flip: bool = False):
    surface_list = []

    for _, dirs, image_files in walk(path):
        for image in sorted(image_files):
            full_path = path + '/' + image

            image_surf = pygame.image.load(full_path).convert_alpha()
            if flip: image_surf = pygame.transform.flip(image_surf, True, False)
            image_surf = scale_image(image_surf, (int(image_surf.get_width()*scale), int(image_surf.get_height()*scale)))
            print(path, image_surf.get_width(), image_surf.get_height())
            surface_list.append(image_surf)

    return surface_list

def get_new_image_size_scale(width: int, new_width: int) -> float:
    return new_width / width

def import_image(path: str) -> pygame.image:
    return pygame.image.load(path).convert_alpha()

def scale_image(image: pygame.image, size: tuple[int, int]) -> pygame.image:
    return pygame.transform.scale(image, size)

def create_bar(size, color):
    max = pygame.Surface(size)
    max.fill(color)
    return max

# Drawing function:
def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))