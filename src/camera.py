import pygame

class Camera():
    def __init__(self, border_right, border_left):
        self.offset = pygame.math.Vector2(0, 0)
        self.border = {
            'left': 0,
            'right': border_right,
            'top': 0,
            'bottom': border_left
        }

    def scroll_camera(self, screen, player_movement):
        half_w = screen.get_size()[0] / 2
        half_h = screen.get_size()[1] / 2
        player = player_movement

        offset_x = self.offset.x
        offset_y = self.offset.y

        # Check X offset
        if self.border['right'] - half_w > player.collision_rect.centerx > half_w:
            offset_x = player.collision_rect.centerx - half_w
        if player.collision_rect.centerx < half_w:
            offset_x = 0
        if player.collision_rect.centerx > self.border['right'] - half_w:
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