import pygame
from support import create_bar, draw_text
from settings import GREY, RED, YELLOW, BLACK, WHITE, NORMAL_FONT, SMALL_STATUS_FONT


class UI:
    def __init__(self):
        # Health bar size:
        self.health_bar_size = [300, 2]

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

    def show_skeletons(self, surface):
        x = surface.get_width() - 120
        y = surface.get_height() - 50
        background = pygame.Surface((110, 45))
        background.fill(BLACK)
        background.set_alpha(180)
        surface.blit(background, (x, y - 5))
        surface.blit(self.skeletons_image, (x, y))
        draw_text(surface, str(int(self.exp_visible)), NORMAL_FONT, GREY, x + 80, y + 20)

    def show_outfit(self, surface, outfit):
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
                draw_text(surface, 'Sword',
                          SMALL_STATUS_FONT, WHITE, positions['sword_pos'][0] + width / 4,
                          positions['sword_pos'][1] + height - 10)
            if item.kind == 'bow':
                surface.blit(item.image, positions['arch_pos']) # Square nr 2 - Bow
                draw_text(surface, 'Bow',
                          SMALL_STATUS_FONT, WHITE, positions['arch_pos'][0] + width / 4,
                          positions['arch_pos'][1] + height - 10)
            if item.kind == 'shield':
                surface.blit(item.image, positions['shield_pos']) # Square nr 3 - Shield
                draw_text(surface, 'Shield',
                          SMALL_STATUS_FONT, WHITE, positions['shield_pos'][0] + width / 4,
                          positions['shield_pos'][1] + height - 10)
            if item.kind == 'item':
                surface.blit(item.image, positions['item_pos'])  # Square nr 4 - Item
                draw_text(surface, 'Item',
                          SMALL_STATUS_FONT, WHITE, positions['item_pos'][0] + width / 4,
                          positions['item_pos'][1] + height - 10)


    def add_experience(self, current, amount):
        self.exp_max = current + amount
        self.exp_visible = current

    def update_experience(self):
        if self.exp_visible < self.exp_max:
            self.exp_visible += 0.5
        else:
            self.exp_visible = int(self.exp_max)
    def show_ui(self, screen, offset, hp: tuple[int, int], sword_cd: tuple[bool, float, int, list], outfit):

        # Health bar:
        self.show_health(screen, hp[0], hp[1])

        # Sword cooldown:
        if not sword_cd[0]:
            self.show_attack_cooldown(screen, sword_cd[1], sword_cd[2],
                                         sword_cd[3], offset)

        # Skeletons:
        self.show_skeletons(screen)
        self.update_experience()

        # Outfit
        self.show_outfit(screen, outfit)
