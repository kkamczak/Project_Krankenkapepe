import pytest
import pygame.rect
import pygame.math
import pygame.sprite
from terrain.collisions import horizontal_movement_collision, vertical_movement_collision

class MockCharacter():
    def __init__(self):
        self.collision_rect = pygame.Rect(100, 100, 80, 40)
        self.on_left = False
        self.on_right = False
        self.on_ground = False
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)
    def apply_gravity(self):
        pass


class MockSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 32, 32)

class TestCollisions():
    @pytest.fixture()
    def data(self):
        sprites = pygame.sprite.Group()
        sprite = MockSprite()
        sprites.add(sprite)
        character = MockCharacter()
        return character, sprites

    def test_collisions__collided_on_left(self, data):
        character = data[0]
        sprites = data[1]
        for sprite in sprites.sprites():
            sprite.rect.center = (16, 16)
        character.collision_rect.center = (50, 16)

        horizontal_movement_collision(character, sprites)

        assert character.collision_rect.left == 32
        assert not character.on_right
        assert character.on_left

    def test_collisions__collided_on_right(self, data):
        character = data[0]
        sprites = data[1]
        for sprite in sprites.sprites():
            sprite.rect.center = (64, 16)
        character.collision_rect.center = (50, 16)

        horizontal_movement_collision(character, sprites)

        assert character.collision_rect.right == 48
        assert character.on_right
        assert not character.on_left

    def test_collisions__collided_on_ground(self, data):
        character = data[0]
        sprites = data[1]
        for sprite in sprites.sprites():
            sprite.rect.centerx = 64
            sprite.rect.top = 100
        character.direction.y = 1
        character.collision_rect.centerx = 64
        character.collision_rect.bottom = 101

        vertical_movement_collision(character, sprites)

        assert character.collision_rect.bottom == 100
        assert character.on_ground
        assert character.direction.y == 0

    def test_collisions__collided_on_ceiling(self, data):
        character = data[0]
        sprites = data[1]
        for sprite in sprites.sprites():
            sprite.rect.centerx = 64
            sprite.rect.bottom = 101
        character.direction.y = -1
        character.collision_rect.centerx = 64
        character.collision_rect.top = 100

        vertical_movement_collision(character, sprites)

        assert character.collision_rect.top == 101
        assert not character.on_ground
        assert character.direction.y == 0
