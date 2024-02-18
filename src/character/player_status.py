from typing import Any


class PlayerStatus:
    def __init__(self, player):
        self.player = player
        self.type = 'management'
        self.id = 999
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
        self.type = 'management'
        self.id = 999
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False

    def get_status(self):
        if self.player.movement.direction.y < 0 and self.get_action() == 'nothing':
            if self.status != 'jump':
                self.player.animations.set_frame_index(0)
            self.status = 'jump'
        elif self.player.movement.direction.y > 1 and self.get_action() == 'nothing':
            if self.status != 'fall':
                self.player.animations.set_frame_index(0)
            self.status = 'fall'
        elif self.get_action() == 'sword':
            if self.status != 'attack':
                self.player.animations.set_frame_index(0)
            self.status = 'attack'
        elif self.get_action() == 'arch':
            if self.status != 'arch':
                self.player.animations.set_frame_index(0)
            self.status = 'arch'
        elif self.get_action() == 'shield':
            if self.status != 'shield':
                self.player.animations.set_frame_index(0)
            self.status = 'shield'
        else:
            if self.player.movement.direction.x != 0:
                if self.status != 'run':
                    self.player.animations.set_frame_index(0)
                self.status = 'run'
            else:
                if self.status != 'idle':
                    self.player.animations.set_frame_index(0)
                self.status = 'idle'

    def get_action(self):
        if not self.player.fighting.attack['attacking'] and \
            not self.player.fighting.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'nothing'
        if self.player.fighting.attack['attacking'] and \
            not self.player.fighting.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'sword'
        if not self.player.fighting.attack['attacking'] and \
            self.player.fighting.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'arch'
        if not self.player.fighting.attack['attacking'] and \
            not self.player.fighting.arch['attacking'] and \
            self.player.defense.shield['shielding']:
            return 'shield'
