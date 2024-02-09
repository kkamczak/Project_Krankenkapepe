import pygame
from typing import Any
from tools.settings import PLAYER_MAX_HEALTH, PLAYER_SIZE, PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP_SPEED, \
    PLAYER_SWORD_COOLDOWN, PLAYER_IMMUNITY_FROM_HIT, SHOW_COLLISION_RECTANGLES, SHOW_IMAGE_RECTANGLES, \
    PLAYER_SHIELD_COOLDOWN, SHOW_PLAYER_STATUS, WHITE, YELLOW, SMALL_STATUS_FONT, SHOW_STATUS_SPACE, PLAYER_ANIMATIONS_PATH, \
    PLAYER_DEATH_ANIMATION_SPEED, PLAYER_SWORD_SPEED, PLAYER_ATTACK_SIZE, PLAYER_ATTACK_SPACE, TILE_SIZE, FPS, \
    PLAYER_ARCH_RANGE, PLAYER_ARCH_COOLDOWN, PLAYER_ARCH_DAMAGE, PLAYER_SWORD_DAMAGE, PLAYER_SWORD_HIT_TIME, \
    PLAYER_ARCH_SPEED, KEY_CD
from tools.support import draw_text, import_character_assets, calculate_animation_speed, now, puts
from tools.game_data import START_ITEMS_LIST
from player.ui import UI
from player.equipment import PlayerEquipment
from terrain.items import create_items
from terrain.tiles import change_loot_priority


class Player(pygame.sprite.Sprite):
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
        # for item in create_items(level, START_ITEMS_LIST, (self, 'player')):
        #     self.equipment.add_item(item)
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
            self.status.get_status()
            self.defense.check_if_hurt()
        self.animations.animate(self.status, self.fighting, self.defense, self.movement)


class PlayerAnimations:
    def __init__(self, player):
        self.player = player
        self.animations_names = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                                 'shield': [], 'arch': []}
        self.animations = {}
        self.flip_animations = {}
        self.image = None
        self.rect = None
        self.frame_index = 0
        self.animation_speed = 0.2

    def set_image(self, new_image: pygame.image) -> None:
        self.image = new_image

    def set_rect(self, new_rect: pygame.Rect) -> None:
        self.rect = new_rect

    def set_frame_index(self, new_index: int) -> None:
        self.frame_index = new_index

    def set_animation_speed(self, new_speed: float) -> None:
        self.animation_speed = new_speed

    def load_animations(self, position):
        self.animations = import_character_assets(self.animations_names.copy(), PLAYER_ANIMATIONS_PATH, scale=TILE_SIZE / 32)
        self.flip_animations = import_character_assets(self.animations_names.copy(), PLAYER_ANIMATIONS_PATH, scale=TILE_SIZE / 32, flip=True)
        self.set_image(self.animations['idle'][self.frame_index])
        self.set_rect(self.image.get_rect(topleft=position))

    def animate(self, player_status, player_attack, player_defence, player_movement):  # Animate method
        animation = self.flip_character(player_status)[player_status.status]

        if player_status.status == 'dead':
            animation_speed = PLAYER_DEATH_ANIMATION_SPEED
        elif player_status.status == 'attack':
            animation_speed = calculate_animation_speed(
                FPS,
                len(animation),
                player_attack.attack['speed']
            )
        elif player_status.status == 'arch':
            animation_speed = calculate_animation_speed(
                FPS,
                len(animation),
                player_attack.arch['speed']
            )
        elif player_status.status == 'shield':
            animation_speed = self.animation_speed
        else:
            animation_speed = self.animation_speed
        # Loop over frame index
        if self.frame_index + animation_speed >= len(animation):
            self.change_status(len(animation) - 1, player_status, player_defence)
        else:
            self.set_frame_index(self.frame_index + animation_speed)

        self.set_image(animation[int(self.frame_index)])
        temp_rect = self.image.get_rect()
        temp_rect.midbottom = player_movement.collision_rect.midbottom
        self.set_rect(temp_rect)

    def change_status(self, new_index, player_status, player_defence):
        if player_status.status == 'dead':
            self.set_frame_index(new_index)
        else:
            if player_status.status == 'shield':  # Is that shield animation?
                player_defence.change_shield_status('shielding', False)
            self.set_frame_index(0)
            player_status.set_status('idle')

    def flip_character(self, player_status):
        if player_status.facing_right:
            return self.animations
        else:
            return self.flip_animations

    def draw(self, surface, offset, player_status, player_movement):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)
        if player_status.can_use_object[0] is True:
            frame = pygame.Surface(player_movement.collision_rect.size)
            frame.fill(YELLOW)
            frame.set_alpha(70)
            surface.blit(frame, player_movement.collision_rect.topleft - offset)

        # ------- FOR DEVELOPING:------------------------------------------------------------------------------------
        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(PLAYER_SIZE)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, player_movement.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)

        if SHOW_PLAYER_STATUS:
            # Show information for developer
            draw_text(surface, 'Pos: ' + str(self.rect.center),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*1 - offset[1])
            draw_text(surface, 'Frame index: ' + str(int(self.frame_index)),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*3 - offset[1])
            draw_text(surface, 'sword_attacking= ' + str(self.player.fighting.attack['attacking']),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 5 - offset[1])
            draw_text(surface, 'sword_able= ' + str(self.player.fighting.attack['able']),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 7 - offset[1])


class PlayerMovement:
    def __init__(self, player):
        self.player = player
        self.direction = None
        self.collision_rect = None
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.on_ground = False
        self.on_left = False
        self.on_right = False
        self.key_pressed = {
            'v': 0
        }

    def set_position(self, position) -> None:
        self.player.animations.rect.midbottom = position
        self.collision_rect.midbottom = position
        self.player.status.set_facing(True)

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

    def init_movement(self):
        self.set_direction(pygame.math.Vector2(0, 0))
        self.set_collision_rect(
            pygame.Rect(
            (self.player.animations.rect.centerx, self.player.animations.rect.top - PLAYER_SIZE[0] / 2),
            PLAYER_SIZE
            )
        )

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
        if keys[pygame.K_s] and \
                self.not_in_fight() and \
                self.player.defense.shield['able'] and \
                not self.player.defense.just_hurt: # Player use SHIELD
            self.player.defense.change_shield_status('shielding', True)
            self.player.defense.change_shield_status('able', False)
            self.player.defense.change_shield_status('start', pygame.time.get_ticks())
        if keys[pygame.K_a] and \
                self.not_in_fight() and \
                self.player.fighting.arch['able'] and \
                now() - self.player.fighting.arch['end'] > self.player.fighting.arch['cooldown']:
            self.player.fighting.arch_start_attack()

    def input_equipment(self, keys):
        if keys[pygame.K_p]: # Key for development testing:
            pass
        if keys[pygame.K_v]: # Change loot priority:
            if now() - self.key_pressed['v'] > KEY_CD['v']:
                change_loot_priority(self.player.status.can_use_object[1])
                self.key_pressed['v'] = now()
                self.player.equipment.close()
        if keys[pygame.K_i]: # Show Equipment
            if pygame.time.get_ticks() - self.player.equipment.show_cooldown > 400:
                if self.player.equipment.show:
                    self.player.equipment.close()
                else:
                    self.player.equipment.open()
                self.player.equipment.loot_window.show_cooldown = pygame.time.get_ticks()
                self.player.equipment.show_cooldown = pygame.time.get_ticks()
        if keys[pygame.K_e]: # Use element:
            index = self.player.status.usable_priority
            if self.player.status.can_use_object[0]:
                element = self.player.status.can_use_object[1][index]
                if element.kind == 'corpse' or element.kind == 'chest':
                    if pygame.time.get_ticks() - self.player.equipment.loot_window.show_cooldown > 400:
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


class PlayerStatus:
    def __init__(self, player):
        self.player = player
        self.type = 'player'
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
        self.type = 'player'
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
            self.attack['damage'] = self.player.equipment.active_items['sword'].damage
        if self.player.equipment.active_items['bow'] is not None:
            self.arch['damage'] = self.player.equipment.active_items['bow'].damage


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
        temp_direction = self.player.movement.direction
        temp_direction.x = 0
        self.player.movement.set_direction(temp_direction)
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
