from tools.settings import LOOT_WIN_SIZE, LOOT_WIN_POS, LOOT_FRAME_SIZE, LOOT_INDEX, LOOT_KIND, LOOT_SPACE, \
    LOOT_HEADER_POS, BUTTON_FONT, WHITE
from tools.support import create_header, draw_text, puts, cursor
from player.frame import Frame


class LootWindow:
    """
    This is class of loot window. It's a temporary container
    for exchanging items between the player and items such as chests or corpses.
    """
    def __init__(self):
        self.header = create_header()
        self.frames = []
        self.show = False
        self.show_cooldown = 0
        self.container = None
        self.create_frames()

    def create_frames(self):
        index = LOOT_INDEX
        for col in range(0, LOOT_WIN_SIZE[1]):
            for row in range(0, LOOT_WIN_SIZE[0]):
                frame = Frame(
                    index,
                    LOOT_KIND,
                    (
                        LOOT_WIN_POS[0] + (LOOT_FRAME_SIZE[0]+LOOT_SPACE) * row,
                        LOOT_WIN_POS[1] + (LOOT_FRAME_SIZE[1]+LOOT_SPACE) * col
                    ),
                    LOOT_FRAME_SIZE
                )
                self.frames.append(frame)
                index += 1

    def load_items(self, items: list, container):
        self.container = container
        if items is None or items == []:
            return
        for item in items:
            for frame in self.frames:
                if frame.kind == 'regular' and frame.item is None:
                    frame.item = item
                    break
        puts('Załadowano itemy do content window')

    def clear_items(self):
        self.container = None
        for frame in self.frames:
            frame.item = None

    def show_window(self, surface):
        if self.show:
            # Show header:
            rect = self.header.get_rect(topleft=(LOOT_HEADER_POS[0], LOOT_HEADER_POS[1]))
            surface.blit(self.header, rect.topleft)
            draw_text(surface, 'Loot', BUTTON_FONT, WHITE, rect.centerx, rect.centery)

            # Show frames:
            info_frame = None

            for frame in self.frames:
                frame.draw(surface)
                if frame.rect.collidepoint(cursor()) and frame.item is not None:
                    info_frame = frame

            if info_frame is not None:
                info_frame.show_info(surface, cursor())


