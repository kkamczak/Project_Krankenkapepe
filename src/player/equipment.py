import pygame
from tools.settings import BLACK, WHITE, EQUIPMENT_POSITION, EQUIPMENT_FRAME_SIZE, EQUIPMENT_FRAME_SPACE, EQUIPMENT_ROWS, \
    EQUIPMENT_COLUMNS, EQUIPMENT_ALPHA, BUTTON_FONT, EQUIPMENT_ACTIVE_POSITION, EQUIPMENT_ACTIVE_FRAME_SIZE, \
    EQUIPMENT_ACTIVE_FRAME_SPACE
from tools.support import draw_text, puts, create_header, cursor
from player.lootwindow import LootWindow
from player.frame import Frame
from terrain import items


class PlayerEquipment:
    def __init__(self, player, items_images) -> None:
        self.player = player
        self.show = False
        self.show_cooldown = pygame.time.get_ticks()
        self.header = create_header()
        self.frames = []
        self.items = []
        self.items_images = items_images
        self.selected_frame = None
        self.active_items = {'sword': None, 'bow': None, 'shield': None, 'item': None}
        self.create_equipment_panel()
        self.loot_window = LootWindow()

    def open(self, both: bool = False):
        self.show = True
        if both:
            self.loot_window.show = True

    def close(self):
        self.loot_window.show = False
        self.loot_window.clear_items()
        self.show = False
        if self.selected_frame is not None:
            self.selected_frame.reset_status()
            self.selected_frame = None

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
        if self.selected_frame != frame:  # If selected frame is not same that before.
            if self.selected_frame is not None:  # If there was already selected frame
                self.selected_frame.change_frame_status()  # Change it status.
                if self.selected_frame.item is not None:  # If there was item on selected frame
                    self.process_transfer(frame)
                else:
                    puts('There was not item to transfer.')
                frame.change_frame_status()
                self.selected_frame = None
            else:
                self.selected_frame = frame  # New selected frame is already clicked frame.
        elif self.selected_frame == frame:  # If selected frame is the same that before.
            self.selected_frame = None # Cancel selected frame.

    def process_transfer(self, frame):
        """
        Function transfers an object from one frame to another.

        :param frame: new frame for item
        :return: None
        """
        item = self.selected_frame.item  # Creates a reference to the object to be transferred
        if frame.item is None:  # Frame is empty - you can put an object in it
            if self.selected_frame.kind == 'regular' and frame.kind == 'active':  # Transfer to active frame
                if frame.name.lower() == item.kind:
                    self.delete_item(item)
                    self.active_item(item)
                    self.selected_frame.item = None
                    puts('Item was succesfully transfered.')
                else:
                    puts('This is not the same kind frame!')
            elif self.selected_frame.kind == 'active' and frame.kind == 'regular':  # Transfer to regular frame
                self.deactivate_item(item, frame)
                self.selected_frame.item = None
                puts('Item was succesfully transfered.')
            elif self.selected_frame.kind == 'regular' and frame.kind == 'regular':  # Transfer to regular frame
                item.active = False
                frame.item = item
                self.selected_frame.item = None
                puts('Item was succesfully transfered.')
            else:
                puts('There was problem with transfering item.')
                return
            if item.owner[1] != 'player' and frame.id < 100:  # Transfer from loot window to equipment
                item.owner[0].equipment.delete_item(item)
                item.owner = (self.player, 'player')
            elif item.owner[1] == 'player' and frame.id >= 100:  # Transfer from equipment to loot window
                item.owner = (self.loot_window.container, self.loot_window.container.kind)
                item.owner[0].equipment.add_item(item)
        else:
            puts('This frame is occupied by other item!')

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

