import pygame
from tools.settings import SCREEN_WIDTH, TILE_SIZE
from tools.support import puts


class Camera():
    def __init__(self, border_right, border_bottom):
        self.offset = pygame.math.Vector2(0, 0)
        self.border = {
            'left': 0,
            'right': border_right,
            'top': 0,
            'bottom': border_bottom
        }
        self.view = [-SCREEN_WIDTH/2-TILE_SIZE, SCREEN_WIDTH/2+TILE_SIZE]

    def scroll_camera(self, screen_size, player_movement):
        half_w = screen_size[0] / 2
        half_h = screen_size[1] / 2
        player = player_movement

        offset_x = self.offset.x
        offset_y = self.offset.y

        # Check X offset
        if self.border['right'] - half_w > player.collision_rect.centerx > half_w:
            self.view = [-half_w-TILE_SIZE, half_w+TILE_SIZE]
            offset_x = player.collision_rect.centerx - half_w
        if player.collision_rect.centerx < half_w:
            self.view = [-half_w*2, half_w*2]
            offset_x = 0
        if player.collision_rect.centerx > self.border['right'] - half_w:
            self.view = [-half_w*2, half_w*2]
            offset_x = self.border['right'] - 2 * half_w
        # Check Y offset
        if self.border['bottom'] - half_h > player.collision_rect.centery > half_h:
            offset_y = player.collision_rect.centery - half_h
        if player.collision_rect.centery < half_h:
            offset_y = 0
        if player.collision_rect.centery > self.border['bottom'] - half_h:
            offset_y = self.border['bottom'] - 2 * half_h

        self.offset.x = offset_x
        self.offset.y = offset_y
