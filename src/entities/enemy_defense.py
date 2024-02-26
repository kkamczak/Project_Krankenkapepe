from tools.settings import ENEMY_IMMUNITY_FROM_HIT, ENEMY_BONUS_BASE
from tools.support import now


class EnemyDefense:
    def __init__(self, enemy):
        # Get hurt:
        self.enemy = enemy
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

    def reset_defense(self, multiplier):
        self.armor_ratio = 1 + ENEMY_BONUS_BASE / 10 * 0.25 * multiplier

    def set_hurt_status(self, new_status: bool) -> None:
        self.just_hurt = new_status

    def set_hurt_time(self, time: int) -> None:
        self.just_hurt_time = time

    def set_armor_ratio(self, new_ratio: float) -> None:
        self.armor_ratio = new_ratio

    def check_if_hurt(self):
        if self.just_hurt:
            if now() - self.just_hurt_time > ENEMY_IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def kill(self) -> None:
        self.enemy.properties.set_dead('status', True)
        self.enemy.properties.set_dead('time', now())
        self.enemy.animations.set_frame_index(0)
        temp_direction = self.enemy.movement.direction
        temp_direction.x = 0
        self.enemy.movement.set_direction(temp_direction)
        self.enemy.status.set_status('dead')

    def hurt(self, damage) -> bool:
        self.just_hurt = True
        self.just_hurt_time = now()
        current_hp = self.enemy.properties.health['current']
        self.enemy.properties.set_health('current', current_hp - damage * self.armor_ratio)
        if self.enemy.properties.health['current'] <= 0:  # Death
            self.kill()
            return True
        return False

    def reset_stun(self):
        self.enemy.status.set_status('run')
        self.enemy.fighting.change_combat_status('stunned', False)
        self.armor_ratio = 1
        self.enemy.fighting.combat_reset()

    def get_stunned(self):
        self.enemy.animations.set_frame_index(0)
        temp_direction = self.enemy.movement.direction
        temp_direction.x = 0
        self.enemy.movement.set_direction(temp_direction)
        self.enemy.fighting.change_combat_status('stunned', True)
        self.enemy.status.set_status('stun')
        self.armor_ratio = 3
