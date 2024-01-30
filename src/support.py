"""
This module contains utility functions for various tasks related to Pygame, file operations,
image processing, and logging.

Functions:
- `import_csv_file(path)`:
Imports a CSV file and returns its content as a list.
- `import_cut_graphics(path: str, size: tuple[int, int]) -> list`:
Loads an image, divides it into tiles, and returns a list of surfaces.
- `import_character_assets(animations, path, scale: float = SCALE, flip: bool = False)`:
Imports character animation assets.
- `import_folder(path: str, scale: float = SCALE, flip: bool = False)`:
Imports images from a folder, scales and flips them as needed, and returns a list of surfaces.
- `get_new_image_size_scale(width: int, new_width: int) -> float`:
Calculates the scale factor for resizing images.
- `import_image(path: str) -> pygame.surface.Surface`:
Imports an image file as a Pygame surface.
- `scale_image(image: pygame.surface.Surface, size: tuple[int, int]) -> pygame.surface.Surface`:
Scales a Pygame surface to a specified size.
- `create_bar(size, color)`:
Creates a Pygame surface representing a colored bar of a specified size and color.
- `draw_text(surface, text, font, text_col, x, y)`:
Draws text on a Pygame surface with a specified font, color, and position.
- `logs_wrapper(func)`:
A decorator that logs function calls, arguments, and return values to a file.
- `puts(text)`:
Logs a message to the console with a timestamp.

This module provides essential functions for handling Pygame graphics,
image processing, and logging.
"""
from csv import reader
from os import walk
from datetime import datetime
import pygame
from settings import SCALE, BUTTON_SIZE

def import_csv_file(path):
    """
    Imports a CSV file and returns its content as a list.

    Args:
    - path (str): The path to the CSV file.

    Returns:
    - list: A list representing the content of the CSV file, where each row is a sub-list.
    """
    terrain_map = []
    with open(path, encoding='utf-8') as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path: str, size: tuple[int, int]) -> list:
    """
    Loads an image, divides it into tiles, and returns a list of surfaces.

    Args:
    - path (str): The path to the image file.
    - size (tuple[int, int]): The size of each tile (width, height).

    Returns:
    - list: A list of Pygame surfaces, each representing a tile from the image.
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / size[0])
    tile_num_y = int(surface.get_size()[1] / size[1])

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x_pos = col * size[0]
            y_pos = row * size[1]
            new_surf = pygame.Surface(size, flags = pygame.SRCALPHA)
            new_surf.blit(
                surface,
                (0, 0),
                pygame.Rect(x_pos, y_pos, size[0], size[1])
            )
            cut_tiles.append(new_surf)

    return cut_tiles


def import_character_assets(animations, path,
                            scale: float = SCALE, flip: bool = False) -> dict:
    """
    Imports character animation assets.

    Args:
    - animations (dict): A dictionary mapping animation names to lists of Pygame surfaces.
    - path (str): The base path to the animation assets folder.
    - scale (float): The scaling factor for the imported images (default is SCALE).
    - flip (bool): Whether to flip the imported images horizontally (default is False).

    Returns:
    - dict: The updated animations dictionary with imported assets.
    """
    for animation in animations.keys():
        full_path = path + animation
        animations[animation] = import_folder(full_path, scale, flip)

    return animations


def import_folder(path: str, scale: float = SCALE, flip: bool = False):
    """
    Imports images from a folder, scales and flips them as needed, and returns a list of surfaces.

    Args:
    - path (str): The path to the folder containing image files.
    - scale (float): The scaling factor for the imported images (default is SCALE).
    - flip (bool): Whether to flip the imported images horizontally (default is False).

    Returns:
    - list: A list of Pygame surfaces, each representing an imported and processed image.
    """
    surface_list = []

    for _, __, image_files in walk(path):
        for image in sorted(image_files):
            full_path = path + '/' + image

            image_surf = pygame.image.load(full_path).convert_alpha()
            if flip:
                image_surf = pygame.transform.flip(image_surf, True, False)
            image_surf = scale_image(
                image_surf,
                (int(image_surf.get_width()*scale), int(image_surf.get_height()*scale))
            )
            surface_list.append(image_surf)

    return surface_list


def get_new_image_size_scale(width: int, new_width: int) -> float:
    """
    Calculates the scale factor for resizing images.

    Args:
    - width (int): The original width of the image.
    - new_width (int): The target width for the resized image.

    Returns:
    - float: The scaling factor to achieve the target width.
    """
    return new_width / width


def import_image(path: str) -> pygame.surface.Surface:
    """
    Imports an image file as a Pygame surface.

    Args:
    - path (str): The path to the image file.

    Returns:
    - pygame.surface.Surface: The loaded image as a Pygame surface.
    """
    return pygame.image.load(path).convert_alpha()


def scale_image(image: pygame.surface.Surface, size: tuple[int, int]) -> pygame.surface.Surface:
    """
    Scales a Pygame surface to a specified size.

    Args:
    - image (pygame.surface.Surface): The Pygame surface to be resized.
    - size (tuple[int, int]): The target size of the surface (width, height).

    Returns:
    - pygame.surface.Surface: The resized Pygame surface.
    """
    return pygame.transform.scale(image, size)


def create_bar(size, color):
    """
    Creates a Pygame surface representing a colored bar.

    Args:
    - size: The size of the bar (width, height).
    - color: The color of the bar.

    Returns:
    - pygame.surface.Surface: The created Pygame surface.
    """
    bar_surface = pygame.Surface(size)
    bar_surface.fill(color)
    return bar_surface


def calculate_animation_speed(fps: int, length: int, cooldown: int) -> float:
    """
    Calculates the length of the animation depending
    on the renewal time and the number of frames of the animation.

    Args:
    - fps: frames per second
    - length: number of animation frames
    - cooldown: cooldown of action

    Returns:
    - float: animation speed
    """

    temp = fps * (cooldown * 1.1 / length) * 1 / 1000
    return 1 / temp


def now() -> int:
    """

    Returns:
    - int: ticks
    """
    return pygame.time.get_ticks()


def create_header():
    """
    Creates header like 'Equipment' or 'Loot'.
    """
    path = 'content/graphics/ui/button.png'
    image = import_image(path)
    image = scale_image(image, BUTTON_SIZE)
    return image


def cursor() -> tuple[int, int]:
    """
    This function returns mouse cursor position.
    """
    return pygame.mouse.get_pos()


# Drawing function:
def draw_text(surface, text, font, text_col, x_pos, y_pos, left=False):
    """
    Draws text on a Pygame surface with a specified font, color, and position.

    Args:
    - surface: The Pygame surface on which to draw the text.
    - text (str): The text to be drawn.
    - font: The Pygame font for rendering the text.
    - text_col: The color of the text.
    - x (int): The x-coordinate of the text's center.
    - y (int): The y-coordinate of the text's center.
    """
    img = font.render(text, True, text_col)
    if not left:
        surface.blit(img, (x_pos - img.get_width() / 2, y_pos - img.get_height() / 2))
    else:
        surface.blit(img, (x_pos, y_pos))


def logs_wrapper(func):
    """
    A decorator that logs function calls, arguments, and return values to a file.

    Args:
    - func: The function to be wrapped and logged.

    Returns:
    - func_with_wrapper: The wrapped function with logging.
    """
    def func_with_wrapper(*args, **kwargs):
        file = open(r'D:\GitHub\Projekt_Krankenkapepe\logs.txt', "a", encoding='utf-8')
        file.write("-" * 30 + "\n")
        file.write(
            f'Function "{func.__name__}" started at '
            f'{datetime.now().strftime("%Y/%m/%d, %H:%M:%S")}'
        )
        file.write("\n")
        file.write('Following arguments were used:')
        file.write("\n")
        file.write(" ".join("{}".format(str(x)) for x in args))
        file.write("\n")
        result = func(*args, **kwargs)
        file.write('Function returned {}\n'.format(result))
        file.close()
        return result
    return func_with_wrapper


def puts(text):
    """
    Logs a message to the console with a timestamp.

    Args:
    - text (str): The message to be logged.
    """
    date_time = datetime.now()
    message = f'[{str(date_time.strftime("%Y/%m/%d, %H:%M:%S"))}] {text}'
    print(message)
