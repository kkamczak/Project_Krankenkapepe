from terrain.tiles import AnimatedTile, TileEquipment


class Portal(AnimatedTile):
    """
    Class for corpse created after defeating enemy.
    """

    def __init__(self, tile_id: int, size: tuple[int, int], position:  tuple, images: list):
        super().__init__(tile_id, size, position[0], position[1], images)
        self.kind = 'portal'
        self.equipment = TileEquipment(True)

    def update(self):
        super().update()
