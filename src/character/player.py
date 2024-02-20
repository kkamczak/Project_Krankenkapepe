from pygame.sprite import Sprite
from management.ui import UI
from character.player_equipment import PlayerEquipment
from character.player_status import PlayerStatus
from character.player_attack import PlayerAttack
from character.player_defense import PlayerDefense
from character.player_properties import PlayerProperties
from character.player_movement import PlayerMovement
from character.player_animations import PlayerAnimations


class Player(Sprite):
    def __init__(self, pos, level):
        super().__init__()

        # Methods:
        self.create_pause = level.create_pause
        self.next_level = level.next_level

        self.animations = PlayerAnimations(self)
        self.movement = PlayerMovement(self)
        self.status = PlayerStatus(self)
        self.fighting = PlayerAttack(self, level.fight_manager.sword_attack, level.fight_manager.arch_attack)
        self.equipment = PlayerEquipment(self, level.images.items)
        self.defense = PlayerDefense(self)
        self.properties = PlayerProperties(self)
        self.ui = UI()

        self.animations.load_animations(pos)
        self.movement.init_movement()
        self.status.reset_status()
        self.fighting.reset_attack_properties()
        self.properties.reset_properties()

    def collect_items(self, items):
        for item in items:
            self.equipment.add_item(item)

    def update(self, screen):
        if not self.properties.dead['status']:
            self.fighting.calculate_damage()
            self.fighting.check_sword_attack_cooldown()
            self.fighting.check_arch_attack_cooldown()
            self.defense.check_shield_cooldown()
            self.movement.get_input()
            self.equipment.update()
            self.status.get_status(self.movement.direction, self.animations.set_frame_index)
            self.defense.check_if_hurt()
        self.animations.animate(self.status, self.fighting, self.defense, self.movement)
