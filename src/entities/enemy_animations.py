import pygame
from tools.settings import GREY, RED, SHOW_IMAGE_RECTANGLES, SHOW_COLLISION_RECTANGLES, \
    SHOW_ENEMY_STATUS, WHITE, FONT_SMALL, SHOW_STATUS_SPACE, ENEMY_ANIMATION_SPEED
from tools.support import draw_text


class EnemyAnimations:
    def __init__(self, enemy):
        self.enemy = enemy
        self.animations = {}
        self.flipped_animations = {}
        self.frame_index = 0
        self.animation_speed = 0
        self.image = None
        self.rect = None

    def set_image(self, new_image: pygame.image) -> None:
        self.image = new_image

    def set_rect(self, new_rect: pygame.Rect) -> None:
        self.rect = new_rect

    def set_frame_index(self, new_index: int) -> None:
        self.frame_index = new_index

    def set_animation_speed(self, new_speed: float) -> None:
        self.animation_speed = new_speed

    def load_animations(self, position, frames):
        type = self.enemy.status.type
        self.animations = frames[0]
        self.flipped_animations = frames[1]
        self.frame_index = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED[type]
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

    def animate(self):
        if self.enemy.status.status == 'attack' or self.enemy.properties.dead['status']:
            return
        animation_speed = self.animation_speed
        animations = self.check_for_flip()
        if self.enemy.defense.just_hurt:
            animation = animations['hit']
        elif self.enemy.fighting.combat['stunned']:
            animation = animations['stun']
            animation_speed = 0.1
        else:
            animation = animations[self.enemy.status.status]

        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.enemy.status.status == 'stun':
                self.enemy.defense.reset_stun()

        self.calculate_rect(animation[int(self.frame_index)])

    def animate_attack(self):
        if self.enemy.status.status == 'attack' and \
                self.enemy.fighting.attack['attacking'] and \
                not self.enemy.properties.dead['status'] and \
                not self.enemy.fighting.combat['stunned']:
            animation_speed = self.enemy.fighting.attack['speed']
            animation = self.check_for_flip()['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > (len(animation) - 1) and self.enemy.fighting.attack['able']:
                self.enemy.fighting.attack['finish'] = True

            if self.frame_index >= len(animation):
                self.enemy.fighting.reset_attack()

            self.calculate_rect(animation[int(self.frame_index)])

    def animate_dead(self):
        if self.enemy.status.status == 'dead' and self.enemy.properties.dead['status']:
            self.enemy.movement.set_direction(x=0, y=0)
            animation_speed = 0.15

            animation = self.check_for_flip()['dead']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1

            self.calculate_rect(animation[int(self.frame_index)])

    def check_for_flip(self):
        if self.enemy.status.facing_right:
            return self.animations
        else:
            return self.flipped_animations

    def calculate_rect(self, animation):
        self.image = animation
        self.rect.midbottom = self.enemy.movement.collision_rect.midbottom
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(self.enemy.movement.collision_rect.size)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, self.enemy.movement.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)

        if SHOW_ENEMY_STATUS:
            # Show information for developer
            draw_text(surface, self.enemy.status.type,
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE * 1 - offset[1])

            draw_text(surface, f'Damage: {str(self.enemy.fighting.attack["damage"])}  HP: {self.enemy.properties.health["current"]}',
                      FONT_SMALL, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE * 3 - offset[1])

            draw_text(surface, 'Level: ' + str(int(self.enemy.properties.level)),
                      FONT_SMALL, WHITE, self.rect.centerx + 5 - offset[0], self.rect.bottom + SHOW_STATUS_SPACE * 5 - offset[1])

    def draw_health_bar(self, screen, offset):
        if not self.enemy.properties.dead['status']:
            rect = self.enemy.movement.collision_rect
            health = self.enemy.properties.health
            hp_max = pygame.Surface((rect.width, 5))
            hp_max.fill(GREY)
            cur = pygame.Surface(
                (health['current'] / health['max'] * rect.width, 5)
            )
            cur.fill(RED)
            screen.blit(hp_max, (rect.left - offset.x, rect.top - 15 - offset.y))
            screen.blit(cur, (rect.left - offset.x, rect.top - 15 - offset.y))
