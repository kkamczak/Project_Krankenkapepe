import pygame

import player
from support import create_bar, draw_text, import_image, scale_image, puts
from settings import GREY, RED, YELLOW, BLACK, NORMAL_FONT, UI_ACTIVE_EQUIPMENT_POSITION, \
    UI_FRAME_SIZE, UI_FRAME_FONT, UI_ITEM_IMAGE_SIZE, UI_HP_BAR_POSITION


class UI:
    def __init__(self):
        # Health bar size:
        self.hp_bar_image = import_image('content/graphics/ui/bar_hp.png')
        self.hp_bar_image = scale_image(self.hp_bar_image, (400, 45))
        self.health_bar_size = [345, 15]

        # Experience:
        self.exp_max = 0
        self.exp_visible = 0

        # Skeletons:
        self.skeletons_image = pygame.image.load('content/graphics/overworld/skeletons.png').convert_alpha()

        # Outfit:


    # Show health
    def show_health(self, surface, hp_max, current):
        #surface.blit(create_bar((self.health_bar_size[0], self.health_bar_size[1]), GREY), (20, 50))
        surface.blit(self.hp_bar_image, UI_HP_BAR_POSITION)
        surface.blit(create_bar((current / hp_max * self.health_bar_size[0], self.health_bar_size[1]), RED), (UI_HP_BAR_POSITION[0]+50, UI_HP_BAR_POSITION[1]+15))

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

    def show_active_equipment(self, surface, active_equipment):
        pos_x = UI_ACTIVE_EQUIPMENT_POSITION[0]
        pos_y = UI_ACTIVE_EQUIPMENT_POSITION[1]
        width = UI_FRAME_SIZE[0]
        height = UI_FRAME_SIZE[1]

        frame = import_image('content/graphics/ui/item_frame.png')
        space = 10

        active_items_frames_positions = {
            'sword_pos' : (pos_x, pos_y - (height + space)),
            'arch_pos' : (pos_x - (width + space), pos_y - (height / 2 + space)),
            'shield_pos' : (pos_x + (width + space), pos_y - (height / 2 + space)),
            'item_pos' : (pos_x, pos_y)
        }
        for position in active_items_frames_positions:
            surface.blit(frame, active_items_frames_positions[position])  # Draw squares

        def show_item_name(key, name):
            draw_text(surface, name,
                      UI_FRAME_FONT, BLACK, active_items_frames_positions[key][0] + width / 3.3,
                      active_items_frames_positions[key][1] + height - 11)

        def get_active_item_position(position: tuple[int, int]) -> list[int, int]:
            new_position = [position[0]+width/2-UI_ITEM_IMAGE_SIZE[0]/2, position[1]+height/2-UI_ITEM_IMAGE_SIZE[1]/2]
            return new_position
        for kind in active_equipment:
            #puts(str(active_equipment))

            if kind == 'sword' and active_equipment[kind] != None:
                surface.blit(active_equipment[kind].image, get_active_item_position(active_items_frames_positions['sword_pos']))  # Square nr 1 - Sword
                show_item_name('sword_pos', 'Sword')
            if kind == 'bow' and active_equipment[kind] != None:
                surface.blit(active_equipment[kind].image, get_active_item_position(active_items_frames_positions['arch_pos'])) # Square nr 2 - Bow
                show_item_name('arch_pos', 'Bow')
            if kind == 'shield' and active_equipment[kind] != None:
                surface.blit(active_equipment[kind].image, get_active_item_position(active_items_frames_positions['shield_pos'])) # Square nr 3 - Shield
                show_item_name('shield_pos', 'Shield')
            if kind == 'item' and active_equipment[kind] != None:
                surface.blit(active_equipment[kind].image, get_active_item_position(active_items_frames_positions['item_pos']))  # Square nr 4 - Item
                show_item_name('item_pos', 'Item')


    def add_experience(self, current, amount):
        self.exp_max = current + amount
        self.exp_visible = current

    def update_experience(self):
        if self.exp_visible < self.exp_max:
            self.exp_visible += 0.5
        else:
            self.exp_visible = int(self.exp_max)
    def show_ui(self, screen, offset, hp: tuple[int, int], sword_cd: tuple[bool, float, int, list], active_equipment, equipment):

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
        self.show_active_equipment(screen, active_equipment)

        #Show equipment:
        if equipment.show:
            equipment.show_equipment(screen)
