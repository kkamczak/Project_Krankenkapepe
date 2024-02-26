import pygame
from typing import Any
from tools.settings import PLAYER_IMMUNITY_FROM_HIT, PLAYER_SHIELD_COOLDOWN
from tools.support import now


class PlayerDefense:
    def __init__(self, player):
        # Taking hits:
        self.player = player
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

        # Shielding:
        self.shield = {
            'shielding': False,
            'able': True,
            'start': 0,
            'cooldown': PLAYER_SHIELD_COOLDOWN
        }

    def set_hurt_status(self, new_status: bool) -> None:
        self.just_hurt = new_status

    def set_hurt_time(self, new_value: int) -> None:
        self.just_hurt_time = new_value

    def set_armor_ratio(self, new_ratio: float) -> None:
        self.armor_ratio = new_ratio

    def change_shield_status(self, key: str, value: Any) -> None:
        self.shield[key] = value

    def check_shield_cooldown(self):
        if not self.shield['able']:
            if (now() - self.shield['start']) > self.shield['cooldown']:
                self.shield['able'] = True
                self.shield['shielding'] = False

    def check_if_hurt(self):
        if self.just_hurt and not self.player.fighting.attack['attacking'] and \
                not self.player.fighting.arch['attacking'] and not self.shield['shielding']:
            self.player.status.set_status('hit')
            if now() - self.just_hurt_time > PLAYER_IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def kill(self) -> None:
        self.player.properties.set_dead('status', True)
        self.player.properties.set_dead('time', pygame.time.get_ticks())
        self.player.animations.set_frame_index(0)
        self.player.movement.set_direction(x=0.0)
        self.player.status.set_status('dead')

    def hurt(self, damage) -> bool:
        self.just_hurt = True
        self.just_hurt_time = pygame.time.get_ticks()
        current_hp = self.player.properties.health['current']
        self.player.properties.set_health('current', current_hp - damage * self.armor_ratio)
        if self.player.properties.health['current'] <= 0:  # Death
            self.kill()
            return True
        return False
