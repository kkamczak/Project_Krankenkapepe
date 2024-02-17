import math
from terrain.tiles import AnimatedTile, TileEquipment
from terrain.items_generator import generate_content_amount, generate_loot_content
from tools.support import puts
from tools.settings import LEVEL_AREA_DISTANCE


class Chest(AnimatedTile):
    """
    Represents a chest tile in the game.

    Chests can contain items and are animated. Players can interact with chests to collect their content.

    Attributes:
        chests (list[Chest]): A list to keep track of all created chest instances.

    Args:
        id (int): The unique identifier for the chest.
        size (tuple[int, int]): The size of the chest (width, height).
        x (int): The x-coordinate of the chest's top-left corner.
        y (int): The y-coordinate of the chest's top-left corner.
        path (str): The path to the folder containing animation frames for the chest.

    Methods:
        animate_once: Animate the chest once and mark it as animated.
        create_content: Create the content (items) for the chest.
        action: Perform an action on the chest (collect its content).
        update: Update the chest's animation frame.
    """

    chests = []

    def __init__(self, id: int, size: tuple[int, int], x: int, y: int, images: list, level_ref) -> None:
        """
        Initialize a Chest object.

        Args:
            id (int): The unique identifier for the chest.
            size (tuple[int, int]): The size of the chest (width, height).
            x (int): The x-coordinate of the chest's top-left corner.
            y (int): The y-coordinate of the chest's top-left corner.
            images (list): List of item images
            level_ref: reference to level map object
        """
        super().__init__(id, size, x, y, images)
        self.kind = 'chest'
        self.level = level_ref.current_level
        self.animated = False
        self.equipment = TileEquipment(True)
        self.equipment.content = create_content([self, 'chest'], level_ref)
        Chest.chests.append(self)

    def animate_once(self) -> None:
        """Animate the chest once, then mark it as animated."""
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
            self.animated = True
        self.image = self.frames[int(self.frame_index)]

    def action(self) -> list:
        """Perform an action on the chest (collect its content)."""
        return self.equipment.content

    def update(self):
        if self.equipment.collected and not self.animated:
            self.animate_once()


def create_content(owner: list, level_ref) -> list:
    """
    Create the content (items) for the container.

    :param owner: object and kind of object in tuple - (object, 'kind')
    :param level_ref: reference to level map object
    :return: list of items
    """
    owner[0].level = math.floor(owner[0].rect.x / LEVEL_AREA_DISTANCE + 1)
    content = generate_loot_content(level_ref, generate_content_amount(), owner)
    return content
