import pygame
from tools.support import import_character_assets
from tools.settings import TILE_SIZE


class Animation(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], kind: str) -> None:
        super().__init__()
        self.position = position
        self.kind = kind
        self.image = None
        self.animations_names = {'default': []}
        self.animations = {}
        self.rect = None
        self.frame_index = 0
        self.animation_speed = 0.15
        self.finish = False

    def load_animations(self, position, path):
        self.animations = import_character_assets(self.animations_names, path, scale=TILE_SIZE / 32)
        self.image = self.animations['default'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

    def animate(self) -> None:
        """Animate the tile by cycling through its frames."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations['default']):
            self.frame_index = 0
        self.image = self.animations['default'][int(self.frame_index)]

    def update(self, offset=None):
        self.animate()

    def draw(self, surface: pygame.Surface, offset: pygame.math.Vector2) -> None:
        """
        Draw the tile on the given surface with the specified offset.

        Args:
            surface (pygame.Surface): The surface to draw the tile on.
            offset (pygame.math.Vector2): The offset to apply to the tile's position.
        """
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)


class SoulAnimation(Animation):
    def __init__(self, position: tuple[int, int], kind: str, target: tuple[int, int]) -> None:
        super().__init__(position, kind)
        self.load_animations(self.position, r'content/graphics/animations/soul/')
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 0.25
        self.target = target

    def update(self, offset) -> None:
        super().update()
        if not self.finish:
            a = self.target[0] + offset.x - self.rect.centerx
            b = self.target[1] + offset.y - self.rect.centery
            c = (a*a + b*b)**(1/2)
            self.direction.x = a / c
            self.direction.y = b / c
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
            self.speed += 0.8
        if self.target[0] + offset.x - self.rect.centerx < 10 or \
            self.target[1] + offset.y - self.rect.centery < 10:
            self.finish = True


