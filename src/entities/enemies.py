import random
import pygame
from tools.settings import ENEMY_ULTIMATE_ATTACK_COOLDOWN
from entities.enemy_animations import EnemyAnimations
from entities.enemy_status import EnemyStatus
from entities.enemy_defense import EnemyDefense
from entities.enemy_properties import EnemyProperties
from entities.enemy_movement import EnemyMovement
from entities.enemy_fighting import EnemyFighting, EnemyFightingThunder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_lvl, enemy_id, pos, kind, frames):
        super().__init__()
        self.status = EnemyStatus(self, kind, enemy_id)
        self.defense = EnemyDefense(self)
        self.animations = EnemyAnimations(self)
        self.properties = EnemyProperties(self, enemy_lvl)
        self.movement = EnemyMovement(self)
        self.fighting = EnemyFighting(self)

        self.multiplier = generate_multiplier(self.properties.level)
        self.status.reset_status()
        self.animations.load_animations(pos, frames)
        self.properties.reset_properties(self.multiplier)
        self.defense.reset_defense(self.multiplier)
        self.fighting.reset_fighting_stats(self.multiplier)
        self.movement.init_movement()

    def update(self):
        if not self.properties.dead['status']:
            self.defense.check_if_hurt()
            self.animations.animate()
        self.animations.animate_dead()
        if not self.status.spawned:
            self.status.set_spawned()


class Sceleton(Enemy):
    def __init__(self, enemy_lvl, enemy_id, pos, frames, sword_attack):
        super().__init__(enemy_lvl, enemy_id, pos, 'sceleton', frames)

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.sword_attack(self)
            self.fighting.change_attack_status('able', False)
            self.fighting.change_attack_status('finish', False)

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class Ninja(Enemy):
    def __init__(self, enemy_lvl, enemy_id, pos, frames, arch_attack):
        super().__init__(enemy_lvl, enemy_id, pos, 'ninja', frames)

        # Methods:
        self.arch_attack = arch_attack

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.arch_attack('arrow', self, target=self.fighting.target)
            self.fighting.change_attack_status('able', False)
            self.fighting.change_attack_status('finish', False)

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class Wizard(Enemy):
    def __init__(self, enemy_lvl, enemy_id, pos, frames, arch_attack, thunder_attack):
        super().__init__(enemy_lvl, enemy_id, pos, 'wizard', frames)
        self.thunder = {
            'time': pygame.time.get_ticks(),
            'cooldown': ENEMY_ULTIMATE_ATTACK_COOLDOWN[self.status.type]
        }
        # Methods:
        self.arch_attack = arch_attack
        self.thunder_attack = thunder_attack

        self.fighting = EnemyFightingThunder(self)
        self.fighting.reset_fighting_stats(self.multiplier)

    def set_thunder(self, key: str, value: int) -> None:
        self.thunder[key] = value

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.arch_attack('death_bullet', self, target=self.fighting.target)
            self.fighting.change_attack_status('able', False)
            self.fighting.change_attack_status('finish', False)

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class DarkKnight(Enemy):
    def __init__(self, enemy_lvl, enemy_id, pos, frames, sword_attack):
        super().__init__(enemy_lvl, enemy_id, pos, 'dark_knight', frames)

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.sword_attack(self)
            self.fighting.change_attack_status('able', False)
            self.fighting.change_attack_status('finish', False)

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


def generate_multiplier(level) -> float:
    multiplier = abs(random.gauss(0, 3) * level)
    return multiplier
