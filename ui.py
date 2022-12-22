import pygame
from support import create_bar, draw_text
from settings import GREY, RED, YELLOW, BLACK, WHITE


class UI:
    def __init__(self):
        # Health bar size:
        self.health_bar_size = [300, 15]

        # Experience:
        self.exp_max = 0
        self.exp_visible = 0

        # Skeletons:
        self.skeletons_image = pygame.image.load('content/graphics/overworld/skeletons.png').convert_alpha()

        # Outfit:


    # Show health
    def show_health(self, surface, hp_max, current):
        surface.blit(create_bar((self.health_bar_size[0], self.health_bar_size[1]), GREY), (20, 50))
        surface.blit(create_bar((current / hp_max * self.health_bar_size[0], self.health_bar_size[1]), RED), (20, 50))

    # Sword cooldown:
    def show_attack_cooldown(self, surface, attack_time, attack_cooldown, collision_rect, offset):

        ratio = (pygame.time.get_ticks() - attack_time) / attack_cooldown
        cd_max = pygame.Surface((collision_rect.width - collision_rect.width * ratio, 5))
        cd_max.fill(YELLOW)

        surface.blit(cd_max, (collision_rect.left - offset.x, collision_rect.top - 15 - offset.y))

    def show_skeletons(self, surface, font):
        x = surface.get_width() - 120
        y = surface.get_height() - 50
        background = pygame.Surface((110, 45))
        background.fill(BLACK)
        background.set_alpha(180)
        surface.blit(background, (x, y - 5))
        surface.blit(self.skeletons_image, (x, y))
        draw_text(surface, str(int(self.exp_visible)), font, GREY, x + 80, y + 20)

    def show_outfit(self, surface, font, outfit):
        pos_x = surface.get_width() / 10
        pos_y = surface.get_height() - 120
        width = 80
        height = 90
        square = pygame.Surface((width - 2, height - 2))
        square.fill(BLACK)
        square.set_alpha(180)

        positions = {
            'sword_pos' : (pos_x, pos_y - height),
            'arch_pos' : (pos_x - width, pos_y - height / 2),
            'shield_pos' : (pos_x + width, pos_y - height / 2),
            'item_pos' : (pos_x, pos_y)
        }
        for pos in positions:
            surface.blit(square, positions[pos])  # Draw squares

        for item in outfit:
            if item.kind == 'sword':
                surface.blit(item.image, positions['sword_pos'])  # Square nr 1 - Sword
            if item.kind == 'bow':
                surface.blit(item.image, positions['arch_pos']) # Square nr 2 - Bow
            if item.kind == 'shield':
                surface.blit(item.image, positions['shield_pos']) # Square nr 3 - Shield
            if item.kind == 'item':
                surface.blit(item.image, positions['item_pos'])  # Square nr 4 - Item


    def add_experience(self, current, amount):
        self.exp_max = current + amount
        self.exp_visible = current

    def update_experience(self):
        if self.exp_visible < self.exp_max:
            self.exp_visible += 0.5
        else:
            self.exp_visible = int(self.exp_max)
