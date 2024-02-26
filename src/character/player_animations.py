import pygame
from tools.settings import PLAYER_SIZE, SHOW_COLLISION_RECTANGLES, SHOW_IMAGE_RECTANGLES, \
    SHOW_PLAYER_STATUS, WHITE, YELLOW, FONT_SMALL, SHOW_STATUS_SPACE, PLAYER_ANIMATIONS_PATH, \
    PLAYER_DEATH_ANIMATION_SPEED, TILE_SIZE, FPS
from tools.support import import_character_assets, calculate_animation_speed, draw_text


class PlayerAnimations:
    def __init__(self, player):
        self.player = player
        self.animations_names = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                                 'shield': [], 'arch': []}
        self.animations = {}
        self.flip_animations = {}
        self.image = None
        self.rect = None
        self.frame_index = 0
        self.animation_speed = 0.2

    def set_image(self, new_image: pygame.image) -> None:
        self.image = new_image

    def set_rect(self, new_rect: pygame.Rect) -> None:
        self.rect = new_rect

    def set_frame_index(self, new_index: int) -> None:
        self.frame_index = new_index

    def set_animation_speed(self, new_speed: float) -> None:
        self.animation_speed = new_speed

    def set_position(self, position: tuple) -> None:
        self.rect.midbottom = position

    def load_animations(self, position: tuple[int, int]) -> None:
        self.animations = import_character_assets(self.animations_names.copy(), PLAYER_ANIMATIONS_PATH, scale=TILE_SIZE / 32)
        self.flip_animations = import_character_assets(self.animations_names.copy(), PLAYER_ANIMATIONS_PATH, scale=TILE_SIZE / 32, flip=True)
        self.set_image(self.animations['idle'][self.frame_index])
        self.set_rect(self.image.get_rect(midbottom=position))

    def animate(self, player_status, player_attack, player_defence, player_movement):  # Animate method
        status = player_status.status
        animation = self.flip_character(player_status)[status]

        if status == 'dead':
            animation_speed = PLAYER_DEATH_ANIMATION_SPEED
        elif status in ('attack', 'arch)'):
            attack_type = 'attack' if status == 'attack' else 'arch'
            speeds = {'attack': player_attack.attack['speed'], 'arch': player_attack.arch['speed'] }
            animation_speed = calculate_animation_speed(FPS, len(animation), speeds[attack_type])
        else:
            animation_speed = self.animation_speed
        # Loop over frame index
        if self.frame_index + animation_speed >= len(animation):
            self.change_status(len(animation) - 1, player_status, player_defence)
        else:
            self.set_frame_index(self.frame_index + animation_speed)

        self.set_image(animation[int(self.frame_index)])
        temp_rect = self.image.get_rect(midbottom=player_movement.collision_rect.midbottom)
        self.set_rect(temp_rect)

    def change_status(self, new_index, player_status, player_defence):
        if player_status.status == 'dead':
            self.set_frame_index(new_index)
        else:
            if player_status.status == 'shield':  # Is that shield animation?
                player_defence.change_shield_status('shielding', False)
            self.set_frame_index(0)
            player_status.set_status('idle')

    def flip_character(self, player_status):
        if player_status.facing_right:
            return self.animations
        else:
            return self.flip_animations

    def draw(self, surface, offset, player_status, player_movement):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)
        if player_status.can_use_object[0] is True:
            frame = pygame.Surface(player_movement.collision_rect.size)
            frame.fill(YELLOW)
            frame.set_alpha(70)
            surface.blit(frame, player_movement.collision_rect.topleft - offset)

        # ------- FOR DEVELOPING:------------------------------------------------------------------------------------
        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(PLAYER_SIZE)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, player_movement.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)

        if SHOW_PLAYER_STATUS:
            # Show information for developer
            draw_text(surface, 'Pos: ' + str(self.rect.center),
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE * 1 - offset[1])
            draw_text(surface, 'Frame index: ' + str(int(self.frame_index)),
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE * 3 - offset[1])
            draw_text(surface, 'sword_attacking= ' + str(self.player.fighting.attack['attacking']),
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 5 - offset[1])
            draw_text(surface, 'sword_able= ' + str(self.player.fighting.attack['able']),
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 7 - offset[1])
