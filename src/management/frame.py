import pygame
from tools.settings import BLACK, WHITE, GREEN, EQUIPMENT_ALPHA, EQUIPMENT_INFO_SIZE, EQUIPMENT_INFO_ALPHA, \
    UI_FRAME_FONT, EQUIPMENT_SHOW_IDS, UI_EQUIPMENT_ACTIVE_FONT
from tools.support import draw_text, scale_image


class Frame(pygame.sprite.Sprite):
    """
    This is a class for a single frame of equipment panel.
    """
    def __init__(self, id: int, kind: str, position: tuple[int, int], size: tuple[int, int], name: str = '') -> None:
        super().__init__()
        self.id = id
        self.kind = kind
        self.position = position
        self.size = size
        self.name = name
        self.item = None
        self.image = pygame.Surface(size)
        self.image.fill(BLACK)
        self.image.set_alpha(EQUIPMENT_ALPHA)
        self.rect = self.image.get_rect(topleft=self.position)

        self.status = {
            'clicked': False,
            'selected': False
        }

    def set_alpha(self, active: bool) -> None:
        """
        Change alpha status of equipment panel frame.

        :param active: Bool value
        :return: None
        """
        if not active:
            self.image.set_alpha(EQUIPMENT_ALPHA)
        else:
            self.image.set_alpha(40)

    def change_frame_status(self) -> None:
        """
        Change active status of equipment panel frame.

        :return: None
        """
        if self.status['selected']:
            self.image.fill(BLACK)
            self.status['selected'] = False
        else:
            self.image.fill(GREEN)
            self.status['selected'] = True
        self.image.set_alpha(EQUIPMENT_ALPHA)

    def reset_status(self) -> None:
        """
        Reset status of frame to not clicked and not selected
        """
        self.status = {
            'clicked': False,
            'selected': False
        }
        self.image.fill(BLACK)
        self.image.set_alpha(EQUIPMENT_ALPHA)

    def check_click(self) -> bool:
        """
        Check if frame is clicked.
        :return: Bool value
        """
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if button active and clicked:
        if self.rect.collidepoint(pos):
            self.set_alpha(True)
            if pygame.mouse.get_pressed()[0] == 1 and not self.status['clicked']:
                self.status['clicked'] = True
                self.change_frame_status()
            elif pygame.mouse.get_pressed()[0] == 0:
                self.status['clicked'] = False
        else:
            self.set_alpha(False)

        return action

    def show_info(self, display_surface: pygame.surface.Surface, position: tuple) -> None:
        """
        Show the items parameters.

        :param display_surface: Main Window
        :param position: Position on screen to display
        :return: None
        """
        size = EQUIPMENT_INFO_SIZE
        frame = pygame.Surface(size)
        frame.fill(WHITE)
        frame.set_alpha(EQUIPMENT_INFO_ALPHA)
        display_surface.blit(frame, position)
        tags = [
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 2 / 30),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 8 / 30),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 14 / 30),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 20 / 30),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 26 / 30),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 32 / 30)
        ]
        draw_text(display_surface, f'Nazwa: {self.item.name}', UI_FRAME_FONT, BLACK, tags[0][0], tags[0][1], left=True)
        draw_text(display_surface, f'{self.item.text}: {self.item.damage}', UI_FRAME_FONT, BLACK, tags[1][0], tags[1][1], left=True)
        draw_text(display_surface, f'Wartość: {self.item.price}', UI_FRAME_FONT, BLACK, tags[2][0], tags[2][1], left=True)
        draw_text(display_surface, f'Id: {self.item.item_id}', UI_FRAME_FONT, BLACK, tags[3][0], tags[3][1], left=True)
        draw_text(display_surface, f'Level: {self.item.level}', UI_FRAME_FONT, BLACK, tags[4][0], tags[4][1], left=True)
        draw_text(display_surface, f'Owner: {self.item.owner[1]}', UI_FRAME_FONT, BLACK, tags[5][0], tags[5][1], left=True)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the frame on the main screen.
        """
        # Draw frame:
        screen.blit(self.image, self.position)
        # Draw frame id:
        if EQUIPMENT_SHOW_IDS:
            draw_text(screen, str(self.id), UI_EQUIPMENT_ACTIVE_FONT, WHITE, self.position[0], self.position[1])
        # Draw frame item:
        if self.item is not None:
            screen.blit(scale_image(self.item.image, self.size), self.position)
        # Draw item name:
        if self.kind == 'active':
            show_item_name(
                screen,
                self.name,
                (
                    int(self.position[0] + self.size[0] * 1 / 4),
                    int(self.position[1] + self.size[1] * 7 / 8)
                )
            )


def show_item_name(surface: pygame.Surface, name: str, position: tuple[int, int]) -> None:
    draw_text(surface, name, UI_EQUIPMENT_ACTIVE_FONT, WHITE, position[0], position[1])
