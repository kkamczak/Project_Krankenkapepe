import pygame
from tools.settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP_SPEED, KEY_DELAY
from tools.support import now
from terrain.tiles import change_loot_priority


class PlayerMovement:
    def __init__(self, player, pos):
        self.player = player
        self.direction = None
        self.collision_rect = self.init_movement(pos)
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.on_ground = False
        self.on_left = False
        self.on_right = False
        self.key_pressed = {
            'v': 0,
            'f': 0
        }

    def set_position(self, position) -> None:
        self.collision_rect.midbottom = position

    def set_direction(self, new_direction: pygame.math.Vector2) -> None:
        self.direction = new_direction

    def set_collision_rect(self, new_rect: pygame.Rect) -> None:
        self.collision_rect = new_rect

    def set_speed(self, new_speed: int) -> None:
        self.speed = new_speed

    def set_gravity(self, new_gravity: float) -> None:
        self.gravity = new_gravity

    def set_jump_speed(self, new_speed: float) -> None:
        self.jump_speed = new_speed

    def set_on_ground(self, new_value: bool) -> None:
        self.on_ground = new_value

    def set_on_left(self, new_value: bool) -> None:
        self.on_left = new_value

    def set_on_right(self, new_value: bool) -> None:
        self.on_right = new_value

    def init_movement(self, pos: tuple) -> pygame.Rect:
        self.set_direction(pygame.math.Vector2(0, 0))
        col_rect = pygame.rect.Rect(pos, PLAYER_SIZE)
        col_rect.midbottom = pos
        return col_rect

    def get_input(self):
        keys = pygame.key.get_pressed()

        self.input_movement(keys)
        self.input_jumping(keys)
        self.input_fighting(keys)
        self.input_equipment(keys)

        if keys[pygame.K_ESCAPE]: # Pause game
            self.player.create_pause()

    def input_movement(self, keys):
        if keys[pygame.K_RIGHT] and self.not_in_fight():
            self.direction.x = 1
            self.player.status.set_facing(True)
            self.player.equipment.close()
        elif keys[pygame.K_LEFT] and self.not_in_fight():
            self.direction.x = -1
            self.player.status.set_facing(False)
            self.player.equipment.close()
        else:
            self.direction.x = 0

    def input_jumping(self, keys):
        if keys[pygame.K_SPACE] and \
                self.on_ground and \
                not self.player.status.just_jumped and \
                self.not_in_fight():
            self.player.movement.jump()
            self.player.status.set_jumped_status(True)
            self.player.equipment.close()
        if not keys[pygame.K_SPACE]: # Player isn't jumping anymore
            self.player.status.set_jumped_status(False)

    def input_fighting(self, keys):
        if keys[pygame.K_d] and \
                self.not_in_fight() and \
                self.player.fighting.attack['able'] and \
                now() - self.player.fighting.attack['end'] > self.player.fighting.attack['cooldown']:
            self.player.fighting.sword_start_attack()
        elif keys[pygame.K_s] and \
                self.not_in_fight() and \
                self.player.defense.shield['able'] and \
                not self.player.defense.just_hurt: # Player use SHIELD
            self.player.defense.change_shield_status('shielding', True)
            self.player.defense.change_shield_status('able', False)
            self.player.defense.change_shield_status('start', pygame.time.get_ticks())
        elif keys[pygame.K_a] and \
                self.not_in_fight() and \
                self.player.fighting.arch['able'] and \
                now() - self.player.fighting.arch['end'] > self.player.fighting.arch['cooldown']:
            self.player.fighting.arch_start_attack()

    def input_equipment(self, keys):
        if keys[pygame.K_p]: # Key for development testing:
            pass
        elif keys[pygame.K_v]: # Change loot priority:
            if now() - self.key_pressed['v'] > KEY_DELAY:
                change_loot_priority(self.player.status.can_use_object[1])
                self.key_pressed['v'] = now()
                self.player.equipment.close()
        elif keys[pygame.K_i]: # Show Equipment
            if now() - self.player.equipment.show_cooldown > KEY_DELAY:
                if self.player.equipment.show:
                    self.player.equipment.close()
                else:
                    self.player.equipment.open()
                self.player.equipment.loot_window.show_cooldown = now()
                self.player.equipment.show_cooldown = now()
        elif keys[pygame.K_e]: # Use element:
            index = self.player.status.usable_priority
            if self.player.status.can_use_object[0]:
                element = self.player.status.can_use_object[1][index]
                if element.kind == 'corpse' or element.kind == 'chest':
                    if now() - self.player.equipment.loot_window.show_cooldown > 400:
                        if self.player.equipment.loot_window.show:
                            self.player.equipment.close()
                        else:
                            self.player.equipment.loot_window.load_items(
                                element.equipment.content,
                                element
                            )
                            self.player.equipment.open(True)
                        self.player.equipment.loot_window.show_cooldown = pygame.time.get_ticks()
                        self.player.equipment.show_cooldown = pygame.time.get_ticks()
                elif element.kind == 'portal':
                    self.player.next_level()
        elif keys[pygame.K_f]: # Use item
            if now() - self.key_pressed['f'] > KEY_DELAY:
                self.key_pressed['f'] = now()
                self.player.equipment.use_item()

    def not_in_fight(self):
        if not self.player.fighting.attack['attacking'] and \
            not self.player.defense.shield['shielding'] and \
            not self.player.fighting.arch['attacking']:
            return True
        return False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
