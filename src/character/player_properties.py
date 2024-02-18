from typing import Any
from tools.settings import PLAYER_MAX_HEALTH


class PlayerProperties:
    def __init__(self, player):
        self.player = player
        self.health = {
            'current': PLAYER_MAX_HEALTH,
            'max': PLAYER_MAX_HEALTH
        }
        self.player_level = 1
        self.experience = {
            'current': 0,
            'max': 300
        }
        self.dead = {
            'status': False,
            'time': 0
        }

    def set_health(self, key: str, value: int) -> None:
        self.health[key] = value

    def add_health(self, value: int) -> None:
        self.health['current'] += value
        if self.health['current'] > self.health['max']:
            self.health['current'] = self.health['max']

    def set_level(self, new_level: int) -> None:
        self.player_level = new_level

    def set_experience(self, key: str, value: Any) -> None:
        self.experience[key] = value

    def set_dead(self, key: str, value: Any):
        self.dead[key] = value

    def reset_properties(self):
        self.health = {
            'current': PLAYER_MAX_HEALTH,
            'max': PLAYER_MAX_HEALTH
        }
        self.player_level = 1
        self.experience = {
            'current': 0,
            'max': 300
        }

    def add_experience(self, experience):
        self.player.ui.add_experience(self.experience['current'], experience)
        self.experience['current'] += experience
