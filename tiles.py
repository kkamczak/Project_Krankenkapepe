import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, id, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.id = id

    def update(self, shift):
        # self.rect.x = self.rect.x - shift.x
        # self.rect.y = self.rect.y - shift.y
        pass

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class StaticTile(Tile):
    def __init__(self, id, size, x, y, surface):
        super().__init__(id, size, x, y)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, id, size, x, y, path):
        super().__init__(id, size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()

        

