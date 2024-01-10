import pygame
from settings import BLACK, WHITE, GREEN, EQUIPMENT_POSITION, EQUIPMENT_FRAME_SIZE, EQUIPMENT_FRAME_SPACE, EQUIPMENT_ROWS, \
    EQUIPMENT_COLUMNS, EQUIPMENT_ALPHA, BUTTON_SIZE, BUTTON_FONT, EQUIPMENT_ACTIVE_POSITION, EQUIPMENT_ACTIVE_FRAME_SIZE, \
    EQUIPMENT_ACTIVE_FRAME_SPACE, UI_EQUIPMENT_ACTIVE_FONT, EQUIPMENT_INFO_SIZE, EQUIPMENT_INFO_ALPHA, UI_FRAME_FONT
from support import import_image, draw_text, scale_image, puts
import items


class Equipment:
    def __init__(self, id: int) -> None:
        self.owner_id = id
        self.show = False
        self.show_cooldown = pygame.time.get_ticks()
        self.header = self.create_header()
        self.frames = []
        self.items = []
        self.selected_frame = None
        self.active_items = {'sword': None, 'bow': None, 'shield': None, 'item': None}
        self.create_equipment_panel()

    def create_header(self):
        path = 'content/graphics/ui/button.png'
        image = import_image(path)
        image = scale_image(image, BUTTON_SIZE)
        return image

    def add_item(self, item: items.Item) -> None:
        if not item.active:
            self.items.append(item)
            for frame in self.frames:
                if frame.kind == 'regular' and frame.item is None:
                    frame.item = item
                    break
        else:
            self.active_item(item)

    def delete_item(self, item: items.Item) -> None:
        for item_owned in self.items:
            if item is item_owned:
                self.items.remove(item_owned)
                break

    def active_item(self, item: items.Item) -> None:
        if self.active_items[item.kind] is not None:
            self.active_items[item.kind].active = False
            self.add_item(self.active_items[item.kind])
        item.active = True
        self.active_items[item.kind] = item
        for frame in self.frames:
            if frame.kind == 'active' and frame.name.lower() == item.kind.lower():
                frame.item = item
                break

    def deactivate_item(self, item: items.Item, frame) -> None:
        if self.active_items[item.kind] == item:
            item.active = False
            self.items.append(item)
            frame.item = item
            self.active_items[item.kind] = None

    def transfer_item(self, frame) -> None:
        if self.selected_frame != frame: # If selected frame is not same that before.
            if self.selected_frame is not None:# If there was already selected frame
                self.selected_frame.change_frame_status() # Change it status.
                if self.selected_frame.item is not None: # If there was item on selected frame
                    item_to_transfer = self.selected_frame.item # Create copy of item to transfer
                    if frame.item is None:
                        if self.selected_frame.kind == 'regular' and frame.kind == 'active':
                            if frame.name.lower() == self.selected_frame.item.kind:
                                self.delete_item(item_to_transfer)
                                self.active_item(item_to_transfer)
                                self.selected_frame.item = None
                                puts('Item was succesfully transfered.')
                            else:
                                puts('This is not the same kind frame!')
                        elif self.selected_frame.kind == 'active' and frame.kind == 'regular':
                            self.deactivate_item(item_to_transfer, frame)
                            self.selected_frame.item = None
                            puts('Item was succesfully transfered.')
                        elif self.selected_frame.kind == 'regular' and frame.kind == 'regular':
                            item_to_transfer.active = False
                            frame.item = item_to_transfer
                            self.selected_frame.item = None
                            puts('Item was succesfully transfered.')
                        else:
                            puts('There was problem with transfering item.')
                    else:
                        puts('This frame is occupied by other item!')
                else:
                    puts('There was not item to transfer.')
                frame.change_frame_status()
                self.selected_frame = None
            else:
                self.selected_frame = frame # New selected frame is already clicked frame.
        elif self.selected_frame == frame: # If selected frame is the same that before.
            self.selected_frame = None # Cancel selected frame.

    def show_equipment(self, display_surface: pygame.surface.Surface) -> None:
        def show_item_name(surface: pygame.Surface, name: str, position: tuple[int, int]) -> None:
            draw_text(surface, name,
                      UI_EQUIPMENT_ACTIVE_FONT, WHITE, position[0], position[1])
        # Show items frames:
        info_pos = None
        info_frame = None
        for frame in self.frames:
            frame.draw(display_surface)
            draw_text(display_surface, str(frame.id), UI_EQUIPMENT_ACTIVE_FONT, WHITE, frame.position[0], frame.position[1])
            pos = pygame.mouse.get_pos()
            if frame.item is not None:
                display_surface.blit(scale_image(frame.item.image, frame.size), frame.position)
                if frame.rect.collidepoint(pos):
                    info_pos = pos
                    info_frame = frame
            if frame.kind == 'active':
                if frame.item is not None:
                    display_surface.blit(scale_image(frame.item.image, frame.size), frame.position)
                    if frame.rect.collidepoint(pos):
                        info_pos = pos
                        info_frame = frame

                show_item_name(display_surface, frame.name,
                               (frame.position[0] + frame.size[0] * 1 / 4, frame.position[1] + frame.size[1] * 7 / 8))
        if info_frame is not None:
            info_frame.show_info(display_surface, info_pos)
        # Show header:
        rect = self.header.get_rect(topleft=(EQUIPMENT_POSITION[0], EQUIPMENT_POSITION[1] - EQUIPMENT_FRAME_SIZE[1]))
        display_surface.blit(self.header, rect.topleft)
        draw_text(display_surface, 'Equipment', BUTTON_FONT, WHITE, rect.centerx, rect.centery)

    def create_equipment_panel(self) -> None:

        # Create items frames:
        id = 0
        (x, y) = EQUIPMENT_POSITION
        size = (width, height) = EQUIPMENT_FRAME_SIZE
        space = EQUIPMENT_FRAME_SPACE

        for row in range(0, EQUIPMENT_ROWS):
            for column in range(0, EQUIPMENT_COLUMNS):
                frame = Frame(id, 'regular', (x + (width + space) * column, y + (height + space) * row), size)
                id += 1
                self.frames.append(frame)

        # Show active items frames:
        (x, y) = EQUIPMENT_ACTIVE_POSITION
        size = (width, height) = EQUIPMENT_ACTIVE_FRAME_SIZE
        space = EQUIPMENT_ACTIVE_FRAME_SPACE
        frame = pygame.Surface(size)
        frame.fill(BLACK)
        frame.set_alpha(EQUIPMENT_ALPHA)

        names = ['Sword', 'Bow', 'Shield', 'Item']
        count = 0
        for row in range(0, 4):
            frame = Frame(id, 'active', (x, y + (height + space) * row), size, names[count])
            id += 1
            count += 1
            self.frames.append(frame)

    def update(self) -> None:
        if self.show:
            for frame in self.frames:
                check = frame.status['selected']
                frame.check_click()
                if check != frame.status['selected']:
                    self.transfer_item(frame)


class Frame(pygame.sprite.Sprite):
    """
    This is a class for a single frame of equipment panel.
    """
    def __init__(self, id: int, kind: str, position: tuple[int, int], size: tuple[int, int], name: str='') -> None:
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
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 2 / 20),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 8 / 20),
            (position[0] + size[0] * 1 / 10, position[1] + size[1] * 14 / 20),
        ]
        draw_text(display_surface, f'Nazwa: {self.item.name}', UI_FRAME_FONT, BLACK, tags[0][0], tags[0][1], left=True)
        draw_text(display_surface, f'{self.item.text}: {self.item.damage}', UI_FRAME_FONT, BLACK, tags[1][0], tags[1][1], left=True)
        draw_text(display_surface, f'Wartość: {self.item.price}', UI_FRAME_FONT, BLACK, tags[2][0], tags[2][1], left=True)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the frame on the main screen.

        :param screen: Main Window
        :return: None
        """

        screen.blit(self.image, self.position)
