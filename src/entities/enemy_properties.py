from typing import Any
from random import choice
from tools.settings import ENEMY_HEALTH, ENEMY_EXPERIENCE, ENEMY_BONUS_BASE


class EnemyProperties:
    def __init__(self, enemy, enemy_lvl):
        self.enemy = enemy
        self.health = {
            'current': ENEMY_HEALTH[self.enemy.status.type],
            'max': ENEMY_HEALTH[self.enemy.status.type]
        }
        self.experience = {
            'current': ENEMY_EXPERIENCE[self.enemy.status.type]
        }
        self.level = generate_level(enemy_lvl)
        self.dead = {
            'status': False,
            'time': 0
        }

    def set_health(self, key: str, value: int) -> None:
        self.health[key] = value

    def set_experience(self, key: str, value: Any) -> None:
        self.experience[key] = value

    def set_dead(self, key: str, value: Any):
        self.dead[key] = value

    def reset_properties(self, multiplier):
        self.health = {
            'current': int(ENEMY_HEALTH[self.enemy.status.type] + 10*ENEMY_BONUS_BASE * multiplier),
            'max': int(ENEMY_HEALTH[self.enemy.status.type] + 10*ENEMY_BONUS_BASE * multiplier)
        }
        self.experience = {
            'current': int(ENEMY_EXPERIENCE[self.enemy.status.type] + ENEMY_BONUS_BASE * multiplier)
        }


def generate_level(level) -> int:
    lvl_list = [level, level+1, level+2]
    return choice(lvl_list)
