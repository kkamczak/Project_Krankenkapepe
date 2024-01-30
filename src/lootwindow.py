from settings import LOOT_WIN_SIZE, LOOT_WIN_POS, LOOT_FRAME_SIZE, LOOT_INDEX, LOOT_KIND, LOOT_SPACE, \
    LOOT_HEADER_POS, BUTTON_FONT, WHITE
from support import create_header, draw_text
from frame import Frame


class LootWindow:

    def __init__(self):
        self.header = create_header()
        self.frames = []
        self.show = False
        self.show_cooldown = 0
        self.content = []
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

    def show_window(self, surface):
        if self.show:
            # Show header:
            rect = self.header.get_rect(topleft=(LOOT_HEADER_POS[0], LOOT_HEADER_POS[1]))
            surface.blit(self.header, rect.topleft)
            draw_text(surface, 'Loot', BUTTON_FONT, WHITE, rect.centerx, rect.centery)

            # Show frames:
            for frame in self.frames:
                frame.draw(surface)


