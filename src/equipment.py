import pygame
from settings import BLACK, WHITE, EQUIPMENT_POSITION, EQUIPMENT_FRAME_SIZE, EQUIPMENT_FRAME_SPACE, EQUIPMENT_ROWS, \
    EQUIPMENT_COLUMNS, EQUIPMENT_ALPHA, BUTTON_SIZE, BUTTON_FONT, EQUIPMENT_ACTIVE_POSITION, EQUIPMENT_ACTIVE_FRAME_SIZE, \
    EQUIPMENT_ACTIVE_FRAME_SPACE, UI_EQUIPMENT_ACTIVE_FONT
from support import import_image, draw_text, scale_image, puts, create_header, cursor
from lootwindow import LootWindow
from frame import Frame
import items


class Equipment:
    def __init__(self, id: int) -> None:
        self.owner_id = id
        self.show = False
        self.show_cooldown = pygame.time.get_ticks()
        self.header = create_header()
        self.frames = []
        self.items = []
        self.selected_frame = None
        self.active_items = {'sword': None, 'bow': None, 'shield': None, 'item': None}
        self.create_equipment_panel()
        self.loot_window = LootWindow()

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

    def show_equipment(self, display_surface: pygame.surface.Surface) -> None:
        # Show items frames:
        info_frame = None
        for frame in self.frames:
            frame.draw(display_surface)
            if frame.rect.collidepoint(cursor()) and frame.item is not None:
                info_frame = frame

        if info_frame is not None:
            info_frame.show_info(display_surface, cursor())

        # Show header:
        rect = self.header.get_rect(topleft=(EQUIPMENT_POSITION[0], EQUIPMENT_POSITION[1] - EQUIPMENT_FRAME_SIZE[1]))
        display_surface.blit(self.header, rect.topleft)
        draw_text(display_surface, 'Equipment', BUTTON_FONT, WHITE, rect.centerx, rect.centery)

        if self.loot_window.show:
            self.loot_window.show_window(display_surface)

    def update(self) -> None:
        if self.show:
            for frame in self.frames:
                check = frame.status['selected']
                frame.check_click()
                if check != frame.status['selected']:
                    self.transfer_item(frame)
            for frame in self.loot_window.frames:
                check = frame.status['selected']
                frame.check_click()
                if check != frame.status['selected']:
                    self.transfer_item(frame)

    def update_show(self, screen):
        if self.show:
            self.show_equipment(screen)

