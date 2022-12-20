import pygame
from support import create_bar, draw_text
from settings import GREY, RED, YELLOW


class UI():
    def __init__(self):
        # Health bar size:
        self.health_bar_size = [300, 15]

        self.exp_max = 0
        self.exp_visable = 0

        # Skeletons:
        self.skeletons_image = pygame.image.load('content/graphics/overworld/skeletons.png').convert_alpha()

    # Show health
    def show_health(self, surface, max, current):
        surface.blit(create_bar((self.health_bar_size[0], self.health_bar_size[1]), GREY), (20, 50))
        surface.blit(create_bar((current / max * self.health_bar_size[0], self.health_bar_size[1]), RED), (20, 50))

    # Sword cooldown:
    def show_attack_cooldown(self, surface, attack_time, attack_cooldown, collision_rect, offset):

        ratio = (pygame.time.get_ticks() - attack_time) / attack_cooldown
        max = pygame.Surface((collision_rect.width - collision_rect.width * ratio, 5))
        max.fill(YELLOW)

        surface.blit(max, (collision_rect.left - offset.x, collision_rect.top - 15 - offset.y))

    def show_skeletons(self, surface, amount, font):
        surface.blit(self.skeletons_image, (10, 80))
        draw_text(surface, str(int(self.exp_visable)), font, GREY, 85, 95)

    def add_experience(self, current, amount):
        self.exp_max = current + amount
        self.exp_visable = current

    def update_experience(self):
        if self.exp_visable < self.exp_max:
            self.exp_visable += 0.5
        else:
            self.exp_visable = int(self.exp_max)