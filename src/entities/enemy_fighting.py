from typing import Any
from tools.settings import ENEMY_ATTACK_SPEED, ENEMY_TRIGGER_LENGTH, ENEMY_ATTACK_SPACE, ENEMY_ATTACK_RANGE, \
    ENEMY_DAMAGE, ENEMY_ATTACK_SIZE, ENEMY_BONUS_BASE, ENEMY_THUNDER_MULTIPLIER
from tools.support import now


class EnemyFighting:
    def __init__(self, enemy):
        self.enemy = enemy
        self.target = None
        # Attacking:
        self.attack = {
            'speed': ENEMY_ATTACK_SPEED[self.enemy.status.type],
            'damage': ENEMY_DAMAGE[self.enemy.status.type],
            'range': ENEMY_ATTACK_RANGE[self.enemy.status.type],
            'size': ENEMY_ATTACK_SIZE[self.enemy.status.type],
            'space': ENEMY_ATTACK_SPACE[self.enemy.status.type],
            'able': True,
            'attacking': False,
            'start': 0,
            'finish': False
        }
        self.combat = {
            'range': ENEMY_TRIGGER_LENGTH[self.enemy.status.type],
            'trigger': False,
            'on': False,
            'start': 0,
            'preparing': 400,
            'stunned': False
        }

    def change_attack_status(self, key: str, new_value: Any) -> None:
        self.attack[key] = new_value

    def change_combat_status(self, key: str, new_value: Any) -> None:
        self.combat[key] = new_value

    def check_for_combat(self, player):
        rect = self.enemy.movement.collision_rect
        height = self.enemy.animations.rect.height
        player_rect = player.movement.collision_rect
        player_dead = player.properties.dead['status']

        dx = abs(rect.centerx - player_rect.centerx)
        dy = abs(rect.centery - player_rect.centery)
        is_close = dx < self.combat['range'] and dy < height
        is_close_to_attack = dx < self.attack['range'] and dy < height

        # --- Enemy will run towards player --
        if is_close and not is_close_to_attack and not self.attack['attacking'] and not player_dead:
            self.combat['trigger'] = True
            temp_dir = self.enemy.movement.direction
            if rect.centerx > player_rect.centerx:
                self.enemy.status.set_facing(False)
                temp_dir.x = -1
            else:
                self.enemy.status.set_facing(True)
                temp_dir.x = 1
            self.enemy.movement.set_direction(temp_dir)
        else:
            self.combat['trigger'] = False

        # --- Enemy will attack player --
        if is_close_to_attack and not self.combat['on'] and not player_dead:
            self.combat['on'] = True
            self.combat['start'] = now()
            self.enemy.status.set_status('idle')
            temp_dir = self.enemy.movement.direction
            temp_dir.x = 0
            self.enemy.movement.set_direction(temp_dir)
            if rect.centerx > player_rect.centerx:
                self.enemy.status.set_facing(False)
            else:
                self.enemy.status.set_facing(True)

        # --- Player runs away --
        if dx > self.combat['range'] and self.combat['on'] and not self.attack['attacking']:
            self.combat_reset()

        # -- Make an attack with weapon
        attack_loaded = now() - self.combat['start'] > self.combat['preparing']
        if self.combat['on'] and attack_loaded and not self.attack['attacking']:
            self.attack['able'] = True
            self.do_attack(player.movement.collision_rect)
        self.target = player_rect.center

    def combat_reset(self):
        self.attack['attacking'] = False
        self.attack['able'] = True
        self.combat['on'] = False
        self.combat['trigger'] = False
        self.enemy.status.set_status('run')

    def do_attack(self, player_pos):
        self.enemy.status.set_status('attack')
        self.attack['attacking'] = True
        self.enemy.animations.set_frame_index(0)

    def reset_attack(self):
        self.enemy.animations.set_frame_index(0)
        self.attack['able'] = True
        self.combat['on'] = False
        self.attack['attacking'] = False
        self.enemy.status.set_status('run')

    def reset_fighting_stats(self, multiplier):
        self.attack['damage'] = int(ENEMY_DAMAGE[self.enemy.status.type] + ENEMY_BONUS_BASE * multiplier)


class EnemyFightingThunder(EnemyFighting):
    def __init__(self, enemy):
        super().__init__(enemy)

    def do_attack(self, player_pos):
        super().do_attack(player_pos)
        if now() - self.enemy.thunder['time'] > self.enemy.thunder['cooldown']:
            self.enemy.thunder_attack(
                'enemy', self.enemy.status.id, player_pos,
                self.enemy.fighting.attack['damage'] * ENEMY_THUNDER_MULTIPLIER, self.enemy.fighting.attack['able']
            )
            self.enemy.set_thunder('time', now())
