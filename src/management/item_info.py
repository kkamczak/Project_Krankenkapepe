from pygame import Surface
from tools.settings import EQUIPMENT_INFO_SIZE, BLACK, WHITE, UI_FRAME_FONT
from tools.support import draw_text
from terrain.items import Item


class ItemInfo:
    """
    This class is responsible for the window with information about the object.
    """
    def __init__(self):
        self.size = EQUIPMENT_INFO_SIZE
        self.frame = self.create_window()

    @staticmethod
    def create_window() -> Surface:
        """
        Create surface for item info.

        :return: Surface
        """
        size = EQUIPMENT_INFO_SIZE
        frame = Surface(size)
        frame.fill(BLACK)
        return frame

    def show_window(self, screen: Surface, pos: tuple, item: Item) -> None:
        """
        Show item info on screen.

        :param screen: main screen
        :param pos: position of window
        :param item: item that info is showed
        :return: None
        """
        space, divider = 4, 30
        information = [
            f'Nazwa: {item.name}',
            f'{item.text}: {item.damage}',
            f'Wartość: {item.price}',
            f'Id: {item.item_id}',
            f'Level: {item.level}',
            f'Owner: {item.owner[1]}'
        ]
        screen.blit(self.frame, pos)
        for index, info in enumerate(information):
            draw_text(
                screen,
                info,
                UI_FRAME_FONT,
                WHITE,
                pos[0] + self.size[0] * 1 / 20,
                pos[1] + self.size[1] * (index + 1) * space / divider,
                left=True
            )
