import pygame
from settings import PLAYER_MAX_HEALTH, PLAYER_SIZE, PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP_SPEED, \
    PLAYER_SWORD_COOLDOWN, PLAYER_IMMUNITY_FROM_HIT, SHOW_COLLISION_RECTANGLES, SHOW_IMAGE_RECTANGLES, \
    PLAYER_SHIELD_COOLDOWN, SHOW_PLAYER_STATUS, WHITE, YELLOW, SMALL_STATUS_FONT, SHOW_STATUS_SPACE, PLAYER_ANIMATIONS_PATH, \
    PLAYER_DEATH_ANIMATION_SPEED, PLAYER_ATTACK_SPEED, PLAYER_ATTACK_SIZE, PLAYER_ATTACK_SPACE, TILE_SIZE
from support import draw_text, import_character_assets
from ui import UI
from items import create_items
from equipment import Equipment
from game_data import START_ITEMS_LIST


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_pause, sword_attack, arch_attack):
        super().__init__()

        self.animations = PlayerAnimations(self)
        self.movement = PlayerMovement(self)
        self.status = PlayerStatus(self)
        self.attack = PlayerAttack(self, sword_attack, arch_attack)
        self.equipment = Equipment(self.status.id)
        self.defense = PlayerDefense(self)
        self.properties = PlayerProperties(self)
        self.ui = UI()

        self.animations.load_animations(pos)
        self.movement.init_movement()
        self.status.reset_status()
        self.attack.reset_attack_properties()
        for item in create_items(START_ITEMS_LIST):
            self.equipment.add_item(item)
        self.properties.reset_properties()

        # Methods:
        self.create_pause = create_pause

    def collect_items(self, items):
        for item in items:
            self.equipment.add_item(item)

    def update(self):
        if not self.properties.dead['status']:
            self.movement.get_input()
            self.equipment.update()
            self.status.get_status()
            self.defense.check_if_hurt()
            self.attack.check_sword_attack_cooldown()
            self.attack.check_arch_attack_cooldown()
            self.defense.check_shield_cooldown()
        self.animations.animate()


class PlayerAnimations():
    def __init__(self, player):
        self.player = player
        self.animations_names = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                                 'shield': [], 'arch': []}
        self.animations = {}
        self.image = None
        self.rect = None
        self.frame_index = 0
        self.animation_speed = 0.2

    def load_animations(self, position):
        self.animations = import_character_assets(self.animations_names, PLAYER_ANIMATIONS_PATH, scale=TILE_SIZE / 32)
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

    def animate(self):  # Animate method

        if self.player.status.status == 'dead':
            animation_speed = PLAYER_DEATH_ANIMATION_SPEED
        elif self.player.status.status == 'attack':
            animation_speed = self.player.attack.sword['speed']
        else:
            animation_speed = self.animation_speed

        animation = self.animations[self.player.status.status]

        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            self.change_status(len(animation) - 1)

        self.flip_character(animation)

    def change_status(self, new_index):
        if self.player.status.status == 'dead':
            self.frame_index = new_index
        else:
            self.frame_index = 0
        if self.player.status.status == 'attack':  # Is that attack animation?
            self.player.status.status = 'idle'
            self.player.attack.sword['attacking'] = False
            self.player.attack.sword['hit'] = True
        if self.player.status.status == 'arch':  # Is that attack animation?
            self.player.attack.arch['finish'] = True
            self.player.status.status = 'idle'
        if self.player.status.status == 'hit':  # Is that hit animation?
            self.player.status.status = 'idle'
        if self.player.status.status == 'shield':  # Is that shield animation?
            self.player.status.status = 'idle'
            self.player.defense.shield['shielding'] = False

    def flip_character(self, animation):
        image = animation[int(self.frame_index)]
        if self.player.status.facing_right:
            self.image = image
            self.rect.midbottom = self.player.movement.collision_rect.midbottom
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.midbottom = self.player.movement.collision_rect.midbottom
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)
        if self.player.status.can_use_object[0] is True:
            frame = pygame.Surface(self.player.movement.collision_rect.size)
            frame.fill(YELLOW)
            frame.set_alpha(70)
            surface.blit(frame, self.player.movement.collision_rect.topleft - offset)

        # ------- FOR DEVELOPING:------------------------------------------------------------------------------------
        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(PLAYER_SIZE)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, self.player.movement.collision_rect.topleft - offset)

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
            draw_text(surface, 'arch_attacking= ' + str(self.player.attack.arch['attacking']),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 5 - offset[1])
            draw_text(surface, 'sword_hit= ' + str(self.player.attack.sword['hit']),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 7 - offset[1])


class PlayerMovement():
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

    def init_movement(self):
        self.direction = pygame.math.Vector2(0, 0)
        self.collision_rect = pygame.Rect(
            (self.player.animations.rect.centerx, self.player.animations.rect.top - PLAYER_SIZE[0] / 2),
            PLAYER_SIZE
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
        if keys[pygame.K_RIGHT] and \
                not self.player.attack.sword['attacking'] and \
                not self.player.defense.shield['shielding'] and \
                not self.player.attack.arch['attacking']:
            self.direction.x = 1
            self.player.status.facing_right = True
        elif keys[pygame.K_LEFT] and \
                not self.player.attack.sword['attacking'] and \
                not self.player.defense.shield['shielding'] and \
                not self.player.attack.arch['attacking']:
            self.direction.x = -1
            self.player.status.facing_right = False
        else:
            self.direction.x = 0

    def input_jumping(self, keys):
        if keys[pygame.K_SPACE] and \
                self.on_ground and \
                not self.player.status.just_jumped and \
                not self.player.attack.sword['attacking'] and \
                not self.player.attack.arch['attacking']:
            self.player.movement.jump()
            self.player.status.just_jumped = True
        if not keys[pygame.K_SPACE]: # Player isn't jumping anymore
            self.player.status.just_jumped = False

    def input_fighting(self, keys):
        if keys[pygame.K_d] and \
                not self.player.attack.sword['attacking'] and \
                not self.player.attack.arch['attacking'] and \
                not self.player.defense.shield['shielding'] and \
                self.player.attack.sword['able']: # Player attack with sword
            self.player.attack.sword_start_attack()
        if keys[pygame.K_s] and \
                not self.player.attack.sword['attacking'] and \
                not self.player.attack.arch['attacking'] and \
                not self.player.defense.shield['shielding'] \
                and self.player.defense.shield['able'] and \
                not self.player.defense.just_hurt: # Player use SHIELD
            self.player.defense.shield['shielding'] = True
            self.player.defense.shield['able'] = False
            self.player.defense.shield['start'] = pygame.time.get_ticks()
        if keys[pygame.K_a] and \
                not self.player.attack.sword['attacking'] and \
                not self.player.attack.arch['attacking'] and \
                not self.player.defense.shield['shielding'] and \
                self.player.attack.sword['able']: # Player shot arrow
            self.player.attack.arch_start_attack()

    def input_equipment(self, keys):
        if keys[pygame.K_i]: # Show Equipment
            if pygame.time.get_ticks() - self.player.equipment.show_cooldown > 400:
                if self.player.equipment.show:
                    self.player.equipment.show = False
                else: self.player.equipment.show = True
                self.player.equipment.show_cooldown = pygame.time.get_ticks()
        if keys[pygame.K_e]: # Use element:
            if self.player.status.can_use_object[0]:
                self.player.status.can_use_object[1].collected = True
                if self.player.status.can_use_object[1].kind == 'chest':
                    self.player.collect_items(self.player.status.can_use_object[1].action())

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed


class PlayerStatus():
    def __init__(self, player):
        self.player = player
        self.type = 'player'
        self.id = 999
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False
        self.can_use_object = [False, None]

    def reset_status(self):
        self.type = 'player'
        self.id = 999
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False

    def get_status(self):
        if self.player.movement.direction.y < 0 and self.get_action() == 'nothing':
            if self.status != 'jump':
                self.player.animations.frame_index = 0
            self.status = 'jump'
        elif self.player.movement.direction.y > 1 and self.get_action() == 'nothing':
            if self.status != 'fall':
                self.player.animations.frame_index = 0
            self.status = 'fall'
        elif self.get_action() == 'sword':
            if self.status != 'attack':
                self.player.animations.frame_index = 0
            self.status = 'attack'
        elif self.get_action() == 'arch':
            if self.status != 'arch':
                self.player.animations.frame_index = 0
            self.status = 'arch'
        elif self.get_action() == 'shield':
            if self.status != 'shield':
                self.player.animations.frame_index = 0
            self.status = 'shield'
        else:
            if self.player.movement.direction.x != 0:
                if self.status != 'run':
                    self.player.animations.frame_index = 0
                self.status = 'run'
            else:
                if self.status != 'idle':
                    self.player.animations.frame_index = 0
                self.status = 'idle'

    def get_action(self):
        if not self.player.attack.sword['attacking'] and \
            not self.player.attack.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'nothing'
        if self.player.attack.sword['attacking'] and \
            not self.player.attack.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'sword'
        if not self.player.attack.sword['attacking'] and \
            self.player.attack.arch['attacking'] and \
            not self.player.defense.shield['shielding']:
            return 'arch'
        if not self.player.attack.sword['attacking'] and \
            not self.player.attack.arch['attacking'] and \
            self.player.defense.shield['shielding']:
            return 'shield'


class PlayerAttack():
    def __init__(self, player, sword_attack, arch_attack):
        self.player = player
        self.sword = {
            'speed': PLAYER_ATTACK_SPEED,
            'attacking': False,
            'start': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'hit': False,
            'damage': 60
        }

        self.arch = {
            'speed': PLAYER_ATTACK_SPEED,
            'attacking': False,
            'start': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'finish': False,
            'damage': 60
        }

        self.sword_attack = sword_attack
        self.arch_attack = arch_attack

    def reset_attack_properties(self):
        self.sword = {
            'speed': PLAYER_ATTACK_SPEED,
            'attacking': False,
            'start': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'hit': False,
            'damage': 60
        }
        self.arch = {
            'speed': PLAYER_ATTACK_SPEED,
            'attacking': False,
            'start': 0,
            'cooldown': PLAYER_SWORD_COOLDOWN,
            'able': True,
            'finish': False,
            'damage': 60
        }

    def sword_start_attack(self):
        self.sword_attack(self.player.status.type, self.player.status.id,
                          self.player.movement.collision_rect,
                          self.player.status.facing_right, self.sword['able'],
                          self.sword['damage'],
                          PLAYER_ATTACK_SPACE, PLAYER_ATTACK_SIZE[1])
        self.sword['start'] = pygame.time.get_ticks()
        self.sword['attacking'] = True
        self.sword['able'] = False

    def arch_start_attack(self):
        self.arch['start'] = pygame.time.get_ticks()
        self.arch['attacking'] = True

    def check_sword_attack_cooldown(self):
        if not self.sword['able']:
            if (pygame.time.get_ticks() - self.sword['start']) > self.sword['cooldown']:
                self.sword['able'] = True
                self.sword['attacking'] = False

    def check_arch_attack_cooldown(self):
        if not self.arch['able']:
            if (pygame.time.get_ticks() - self.arch['start']) > self.arch['cooldown']:
                self.arch['able'] = True
                self.arch['attacking'] = False
        if self.arch['finish']:
            self.arch_attack('arrow', 'player', self.player.status.id, self.player.movement.collision_rect,
                                    self.player.status.facing_right, self.arch['damage'],
                                    self.arch['able'])
            self.arch['able'] = False
            self.arch['attacking'] = False
            self.arch['finish'] = False


class PlayerDefense():
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
    def check_shield_cooldown(self):
        if not self.shield['able']:
            if (pygame.time.get_ticks() - self.shield['start']) > self.shield['cooldown']:
                self.shield['able'] = True
                self.shield['shielding'] = False

    def check_if_hurt(self):
        if self.just_hurt and not self.player.attack.sword['attacking'] and \
                not self.player.attack.arch['attacking'] and not self.shield['shielding']:
            self.player.status.status = 'hit'
            if pygame.time.get_ticks() - self.just_hurt_time > PLAYER_IMMUNITY_FROM_HIT:
                self.just_hurt = False


class PlayerProperties():
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