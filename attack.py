import pygame
from settings import RED, ATTACK_SIZE, SHOW_HIT_RECTANGLES

class Hit(pygame.sprite.Sprite):
    def __init__(self, pos, damage, source, source_id, width):
        super().__init__()
        # Create surface
        self.source = source
        self.source_id = source_id
        size = ATTACK_SIZE
        size[0] = width

        self.image = pygame.Surface(size)
        self.image.fill(RED)
        if SHOW_HIT_RECTANGLES: self.image.set_alpha(50)
        else: self.image.set_alpha(0)

        self.rect = self.image.get_rect(topleft = pos)

        self.attack_time = pygame.time.get_ticks()
        self.attack_duration = 100

        self.damage = damage
        self.shielded = False

    def update(self):
        pass
    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, damage, source, facing_right):
        super().__init__()

        self.source = source

        self.image = pygame.image.load('content/graphics/weapons/arrow.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect((pos), (5, 5))

        self.facing_right = facing_right

        if not self.facing_right:
            self.direction = pygame.math.Vector2(-1, 0)
        else:
            self.direction = pygame.math.Vector2(1, 0)
            flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = flipped_image

        self.speed = 10

        self.attack_time = pygame.time.get_ticks()
        self.attack_duration = 1500

        self.damage = damage
        self.shielded = False

    def update(self):
        self.collision_rect.x += self.direction.x * self.speed
        if self.facing_right:
            self.rect.topright = self.collision_rect.topright
            self.rect = self.image.get_rect(topright=self.rect.topright)
        else:
            self.rect.topleft = self.collision_rect.topleft
            self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)