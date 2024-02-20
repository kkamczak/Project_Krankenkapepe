from typing import Any, Callable
from pygame.math import Vector2


class PlayerStatus:
    def __init__(self):
        self.type = 'player'
        self.id = 999
        self.previous_status = 'idle'
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False
        self.can_use_object = [False, None]
        self.usable_priority = 0

    def set_status(self, new_status: str) -> None:
        self.status = new_status

    def set_facing(self, new_facing: bool) -> None:
        self.facing_right = new_facing

    def set_jumped_status(self, new_status: bool) -> None:
        self.just_jumped = new_status

    def set_object_usable(self, can_use: list[bool, Any]) -> None:
        self.can_use_object = can_use

    def reset_status(self):
        self.type = 'player'
        self.id = 999
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False
        self.can_use_object = [False, None]
        self.usable_priority = 0

    def get_status(self, direction: Vector2, set_frame: Callable[[int], None], sword: bool, arch: bool, shield: bool) -> None:
        """
        There, the method checks the player's current activity.

        :param direction: movement direction of player
        :param set_frame: player animations method that change frame index
        :param sword: sword attack status
        :param arch: arch attack status
        :param shield: shield defense status
        :return: none
        """
        action = self.get_action(sword, arch, shield)
        if direction.y < 0 and action == 'nothing':
            new_status = 'jump'
        elif direction.y > 1 and action == 'nothing':
            new_status = 'fall'
        elif action == 'sword':
            new_status = 'attack'
        elif action == 'arch':
            new_status = 'arch'
        elif action == 'shield':
            new_status = 'shield'
        else:
            if direction.x != 0:
                new_status = 'run'
            else:
                new_status = 'idle'
        if self.status != new_status:
            set_frame(0)
        self.status = new_status

    @staticmethod
    def get_action(sword: bool, arch: bool, shield: bool) -> str:
        """
        Checks whether the player is in one of the states indicating participation in combat

        :param sword: sword attack status
        :param arch: arch attack status
        :param shield: shield defense status
        :return: None
        """
        if not sword and not arch and not shield:
            return 'nothing'
        if sword and not arch and not shield:
            return 'sword'
        if not sword and arch and not shield:
            return 'arch'
        if not sword and not arch and shield:
            return 'shield'
