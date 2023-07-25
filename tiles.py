import pygame
from support import import_folder, puts
from game_data import CHESTS_CONTENT
from items import create_items

class Tile(pygame.sprite.Sprite):
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int) -> None:
        super().__init__()
        self.kind = 'terrain'
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
        self.usable = False

    def animate(self) -> None:
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        self.animate()

class Chest(AnimatedTile):
    chests = []
    def __init__(self, id: int, size: tuple[int, int], x: int, y: int, path: str) -> None:
        super().__init__(id, size, x, y, path)
        self.kind = 'chest'
        self.collected = False
        self.animated = False
        self.usable = True
        self.content = self.create_content()
        puts(f'Stworzono skrzynie, id {self.id}')
        Chest.chests.append(self)
    def animate_once(self) -> None:
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
            self.animated = True
        self.image = self.frames[int(self.frame_index)]
    def create_content(self) -> list:
        content = []
        # puts(str(Chest.chests))
        # for i, element in enumerate(Chest.chests):
        #     puts(f'Tworzenie ekwipunku skrzyni o id: {element.id}')
        #     for item in create_items(CHESTS_CONTENT[i]):
        #         content.append(item)
        puts(str(len(Chest.chests)))
        for element in create_items(CHESTS_CONTENT[len(Chest.chests)]):
            content.append(element)
        return content
    def action(self) -> list:
        return self.content
    def update(self):
        if self.collected and not self.animated:
            self.animate_once()

def check_for_usable_elements(character, elements) -> list:
    for element in elements:
        if not element.usable: continue
        if abs(character.rect.centerx - element.rect.centerx) < 50 and \
            abs(character.rect.centery - element.rect.centery) < 50 and \
            not element.collected:
            return [True, element]
    return [False, None]

