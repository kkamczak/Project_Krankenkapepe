import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.id = id

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface, offset: pygame.math.Vector2) -> None:
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class StaticTile(Tile):
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int, surface: pygame.Surface) -> None:
        super().__init__(id, size, x, y)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int, path: str) -> None:
        super().__init__(id, size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self) -> None:
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        self.animate()

        

