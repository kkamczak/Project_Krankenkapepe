from typing import Any
from tools.settings import PLAYER_SWORD_COOLDOWN, PLAYER_SWORD_SPEED, PLAYER_ATTACK_SIZE, PLAYER_ATTACK_SPACE, \
    PLAYER_ARCH_RANGE, PLAYER_ARCH_COOLDOWN, PLAYER_ARCH_DAMAGE, PLAYER_SWORD_DAMAGE, PLAYER_SWORD_HIT_TIME, \
    PLAYER_ARCH_SPEED
from tools.support import now


class PlayerAttack:
    def __init__(self, player, sword_attack, arch_attack):
        self.player = player
        self.attack = {
            'speed': PLAYER_SWORD_SPEED,
            'attacking': False,
            'start': 0,
            'end': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'hit': False,
            'damage': PLAYER_SWORD_DAMAGE,
            'space': PLAYER_ATTACK_SPACE,
            'size': PLAYER_ATTACK_SIZE
        }

        self.arch = {
            'speed': PLAYER_ARCH_SPEED,
            'range': PLAYER_ARCH_RANGE,
            'attacking': False,
            'start': 0,
            'end': 0,
            'cooldown': PLAYER_ARCH_COOLDOWN,
            'able': True,
            'damage': PLAYER_ARCH_DAMAGE
        }

        self.sword_attack = sword_attack
        self.arch_attack = arch_attack

    def change_attack_status(self, key: str, new_value: Any) -> None:
        self.attack[key] = new_value

    def change_arch_status(self, key: str, new_value: Any) -> None:
        self.arch[key] = new_value

    def reset_attack_properties(self):
        self.attack = {
            'speed': PLAYER_SWORD_SPEED,
            'attacking': False,
            'start': 0,
            'end': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'hit': False,
            'damage': PLAYER_SWORD_DAMAGE,
            'space': PLAYER_ATTACK_SPACE,
            'size': PLAYER_ATTACK_SIZE
        }
        self.arch = {
            'speed': PLAYER_ARCH_SPEED,
            'range': PLAYER_ARCH_RANGE,
            'attacking': False,
            'start': 0,
            'end': 0,
            'cooldown': PLAYER_ARCH_COOLDOWN,
            'able': True,
            'damage': PLAYER_ARCH_DAMAGE
        }

    def sword_start_attack(self):
        self.attack['start'] = now()
        self.attack['attacking'] = True
        self.attack['able'] = False

    def arch_start_attack(self):
        self.arch['start'] = now()
        self.arch['attacking'] = True
        self.arch['able'] = False

    def check_sword_attack_cooldown(self):
        if self.attack['attacking'] and \
                (now() - self.attack['start']) > PLAYER_SWORD_HIT_TIME * self.attack['speed']:
            if not self.attack['hit']:
                self.sword_attack(self.player)
                self.attack['hit'] = True
            if (now() - self.attack['start']) > self.attack['speed']:
                self.attack['able'] = True
                self.attack['attacking'] = False
                self.attack['hit'] = False
                self.attack['end'] = now()

    def check_arch_attack_cooldown(self):
        if self.arch['attacking'] and \
                (now() - self.arch['start']) > self.arch['speed']:
            self.arch_attack('arrow', self.player)
            self.arch['able'] = True
            self.arch['attacking'] = False
            self.arch['end'] = now()

    def calculate_damage(self) -> None:
        if self.player.equipment.active_items['sword'] is not None:
            self.attack['damage'] = PLAYER_SWORD_DAMAGE + self.player.equipment.active_items['sword'].damage
        else:
            self.attack['damage'] = PLAYER_SWORD_DAMAGE
        if self.player.equipment.active_items['bow'] is not None:
            self.arch['damage'] = PLAYER_ARCH_DAMAGE + self.player.equipment.active_items['bow'].damage
        else:
            self.arch['damage'] = PLAYER_ARCH_DAMAGE
