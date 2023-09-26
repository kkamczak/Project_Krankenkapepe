"""
This module defines the UI (User Interface) class for displaying various game-related information,
including health bars, cooldowns, equipment, and more.

It provides methods to display and update these UI elements during gameplay.
"""
import pygame
import equipment
from support import create_bar, draw_text, import_image, scale_image
from settings import GREY, RED, YELLOW, BLACK, NORMAL_FONT, UI_ACTIVE_EQUIPMENT_POSITION, \
    UI_FRAME_SIZE, UI_FRAME_FONT, UI_ITEM_IMAGE_SIZE, UI_HP_BAR_POSITION


class UI:
    """
    This class represents the user interface (UI) elements in the game,
    such as health bars, equipment display, and more.
    """

    def __init__(self) -> None:
        """
        Initialize the UI elements.

        Args:
            None

        Returns:
            None
        """
        # Health bar size:
        self.hp_bar_image = import_image('content/graphics/ui/bar_hp.png')
        self.hp_bar_image = scale_image(self.hp_bar_image, (400, 45))
        self.health_bar_size = [345, 15]

        # Experience:
        self.exp_max = 0
        self.exp_visible = 0

        # Skeletons:
        self.skeletons_image = pygame.image.load(
            'content/graphics/overworld/skeletons.png').convert_alpha()

    def show_health(self, surface: pygame.surface.Surface, hp_max: int, current: int) -> None:
        """
        Display the player's health bar on the given surface.

        Args:
            surface: The surface to display the health bar on.
            hp_max: The maximum health points.
            current: The current health points.

        Returns:
            None
        """
        # surface.blit(
        #     create_bar((self.health_bar_size[0], self.health_bar_size[1]), GREY),
        #     (20, 50)
        # )
        surface.blit(self.hp_bar_image, UI_HP_BAR_POSITION)
        surface.blit(
            create_bar((current / hp_max * self.health_bar_size[0], self.health_bar_size[1]), RED),
            (UI_HP_BAR_POSITION[0]+50, UI_HP_BAR_POSITION[1]+15)
        )

    def show_attack_cooldown(self, surface: pygame.surface.Surface,
                            attack_time: int, attack_cooldown: int,
                            collision_rect: pygame.Rect, offset: pygame.math.Vector2) -> None:
        """
        Display the cooldown bar for player attacks on the given surface.

        Args:
            surface: The surface to display the cooldown bar on.
            attack_time: The time of the last attack.
            attack_cooldown: The cooldown time for attacks.
            collision_rect: The collision rectangle.
            offset: The offset for rendering.

        Returns:
            None
        """
        ratio = (pygame.time.get_ticks() - attack_time) / attack_cooldown
        cd_max = pygame.Surface((collision_rect.width - collision_rect.width * ratio, 5))
        cd_max.fill(YELLOW)

        surface.blit(cd_max, (collision_rect.left - offset.x, collision_rect.top - 15 - offset.y))

    def show_skeleton_points(self, surface: pygame.surface.Surface) -> None:
        """
        Display information about skeleton points on the given surface.

        Args:
            surface: The surface to display skeleton points information on.

        Returns:
            None
        """
        x_pos = surface.get_width() - 120
        y_pos = surface.get_height() - 50
        background = pygame.Surface((110, 45))
        background.fill(BLACK)
        background.set_alpha(180)
        surface.blit(background, (x_pos, y_pos - 5))
        surface.blit(self.skeletons_image, (x_pos, y_pos))
        draw_text(surface, str(int(self.exp_visible)), NORMAL_FONT, GREY, x_pos + 80, y_pos + 20)

    def show_active_equipment(self, surface: pygame.surface.Surface,
                              active_equipment: dict) -> None:
        """
        Display the player's active equipment on the given surface.

        Args:
            surface: The surface to display equipment on.
            active_equipment: Dictionary containing active equipment items.

        Returns:
            None
        """
        pos_x = UI_ACTIVE_EQUIPMENT_POSITION[0]
        pos_y = UI_ACTIVE_EQUIPMENT_POSITION[1]
        width = UI_FRAME_SIZE[0]
        height = UI_FRAME_SIZE[1]

        frame = import_image('content/graphics/ui/item_frame.png')
        space = 10

        active_items_frames_positions = {
            'sword_pos' : (pos_x, pos_y - (height + space)),
            'arch_pos' : (pos_x - (width + space), pos_y - (int(height / 2) + space)),
            'shield_pos' : (pos_x + (width + space), pos_y - (int(height / 2) + space)),
            'item_pos' : (pos_x, pos_y)
        }
        # for position in active_items_frames_positions:
        #     surface.blit(frame, active_items_frames_positions[position])  # Draw squares
        for _, position in active_items_frames_positions.items():
            surface.blit(frame, position)  # Draw squares

        def show_item_name(key, name):
            draw_text(surface, name,
                      UI_FRAME_FONT, BLACK, active_items_frames_positions[key][0] + width / 3.3,
                      active_items_frames_positions[key][1] + height - 11)

        def get_active_item_position(position: tuple[int, int]) -> list[int]:
            new_position = [
                int(position[0]+width/2-UI_ITEM_IMAGE_SIZE[0]/2),
                int(position[1]+height/2-UI_ITEM_IMAGE_SIZE[1]/2)
            ]
            return new_position
        for kind in active_equipment:
            #puts(str(active_equipment))

            if kind == 'sword' and active_equipment[kind] is not None:
                surface.blit(
                    active_equipment[kind].image,
                    get_active_item_position(active_items_frames_positions['sword_pos'])
                )  # Square nr 1 - Sword
                show_item_name('sword_pos', 'Sword')
            if kind == 'bow' and active_equipment[kind] is not None:
                surface.blit(
                    active_equipment[kind].image,
                    get_active_item_position(active_items_frames_positions['arch_pos'])
                ) # Square nr 2 - Bow
                show_item_name('arch_pos', 'Bow')
            if kind == 'shield' and active_equipment[kind] is not None:
                surface.blit(
                    active_equipment[kind].image,
                    get_active_item_position(active_items_frames_positions['shield_pos'])
                ) # Square nr 3 - Shield
                show_item_name('shield_pos', 'Shield')
            if kind == 'item' and active_equipment[kind] is not None:
                surface.blit(
                    active_equipment[kind].image,
                    get_active_item_position(active_items_frames_positions['item_pos'])
                )  # Square nr 4 - Item
                show_item_name('item_pos', 'Item')

    def add_experience(self, current: int, amount: int) -> None:
        """
        Add experience points to the player's current experience.

        Args:
            current: The current experience points.
            amount: The amount of experience points to add.

        Returns:
            None
        """
        self.exp_max = current + amount
        self.exp_visible = current

    def update_experience(self) -> None:
        """
        Update the visible experience points on the UI.

        Args:
            None

        Returns:
            None
        """
        if self.exp_visible < self.exp_max:
            self.exp_visible += 1
        else:
            self.exp_visible = int(self.exp_max)

    def show_ui(self, screen: pygame.surface.Surface,
                offset: pygame.math.Vector2, health: tuple[int, int],
                sword_cd: tuple[bool, int, int, pygame.Rect],
                active_equipment: dict, player_equipment: equipment.Equipment) -> None:
        """
        Display the entire user interface on the screen.

        Args:
            screen: The screen surface to display the UI on.
            offset: The offset for rendering.
            health: Tuple containing maximum health and current health.
            sword_cd: Tuple containing sword cooldown information.
            active_equipment: Dictionary containing active equipment items.
            player_equipment: The player's equipment.

        Returns:
            None
        """

        # Health bar:
        self.show_health(screen, health[0], health[1])

        # Sword cooldown:
        if not sword_cd[0]:
            self.show_attack_cooldown(screen, sword_cd[1], sword_cd[2],
                                         sword_cd[3], offset)

        # Skeletons:
        self.show_skeleton_points(screen)
        self.update_experience()

        # Outfit
        self.show_active_equipment(screen, active_equipment)

        #Show equipment:
        if player_equipment.show:
            player_equipment.show_equipment(screen)
