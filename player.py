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

        self.animations.load_animations(pos)
        self.movement.init_movement()

        # Player status:
        self.type = 'player'
        self.id = 999
        self.status = 'idle'
        self.facing_right = True
        self.just_jumped = False

        # Attacking with Sword:
        self.attack_speed = PLAYER_ATTACK_SPEED
        self.sword_attacking = False  # Is player on sword attack animation?
        self.sword_attack_time = 0  # When did player attack?
        self.sword_attack_cooldown = PLAYER_SWORD_COOLDOWN  # What is cooldown for sword attack?
        self.sword_can_attack = True  # Can player attack?
        self.sword_hit = False

        # Attacking with Arch
        self.arch_attacking = False
        self.arch_attack_time = 0
        self.arch_attack_cooldown = PLAYER_SWORD_COOLDOWN
        self.arch_can_attack = True
        self.arch_attack_finish = False

        # Taking hits:
        self.just_hurt = False
        self.just_hurt_time = 0

        # Shielding:
        self.shielding = False
        self.can_shield = True
        self.shield_time = 0
        self.shield_cooldown = PLAYER_SHIELD_COOLDOWN

        # Properties:
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.armor_ratio = 1

        # Experience:
        self.player_level = 1
        self.max_exp = 300
        self.experience = 0

        # Damage:
        self.sword_damage = 60
        self.arch_damage = 50

        # Death:
        self.dead = False
        self.dead_time = 0

        # Methods:
        self.create_pause = create_pause
        self.player_sword_attack = sword_attack
        self.player_arch_attack = arch_attack

        # Start items:
        self.equipment = Equipment(self.id)
        for item in create_items(START_ITEMS_LIST):
            self.equipment.add_item(item)

        # Object integration
        self.can_use_object = [False, None]

        # Create in-level UI:
        self.ui = UI()

    def get_status(self):
        if self.movement.direction.y < 0 and not self.sword_attacking and not self.shielding:
            if self.status != 'jump':
                self.animations.frame_index = 0
            self.status = 'jump'
        elif self.movement.direction.y > 1 and not self.sword_attacking and not self.shielding:
            if self.status != 'fall':
                self.animations.frame_index = 0
            self.status = 'fall'
        elif self.sword_attacking and not self.shielding and not self.arch_attacking:
            if self.status != 'attack':
                self.animations.frame_index = 0
            self.status = 'attack'
        elif not self.sword_attacking and not self.shielding and self.arch_attacking:
            if self.status != 'arch':
                self.animations.frame_index = 0
            self.status = 'arch'
        elif not self.sword_attacking and not self.arch_attacking and self.shielding:
            if self.status != 'shield':
                self.animations.frame_index = 0
            self.status = 'shield'
        else:
            if self.movement.direction.x != 0:
                if self.status != 'run':
                    self.animations.frame_index = 0
                self.status = 'run'
            else:
                if self.status != 'idle':
                    self.animations.frame_index = 0
                self.status = 'idle'

    def sword_attack(self):
        self.player_sword_attack(self.type, self.id, self.movement.collision_rect, self.facing_right, self.sword_damage,
                                 self.sword_can_attack, self.movement.collision_rect.width, PLAYER_ATTACK_SPACE, PLAYER_ATTACK_SIZE[1])
        self.sword_attack_time = pygame.time.get_ticks()
        self.sword_attacking = True
        self.sword_can_attack = False

    def arch_attack(self):
        self.arch_attack_time = pygame.time.get_ticks()
        self.arch_attacking = True

    def check_sword_attack_cooldown(self):
        if not self.sword_can_attack:
            if (pygame.time.get_ticks() - self.sword_attack_time) > self.sword_attack_cooldown:
                self.sword_can_attack = True
                self.sword_attacking = False

    def check_arch_attack_cooldown(self):
        if not self.arch_can_attack:
            if (pygame.time.get_ticks() - self.arch_attack_time) > self.arch_attack_cooldown:
                self.arch_can_attack = True
                self.arch_attacking = False
        if self.arch_attack_finish:
            self.player_arch_attack('arrow', 'player', self.id, self.movement.collision_rect, self.facing_right, self.arch_damage,
                                    self.arch_can_attack)
            self.arch_can_attack = False
            self.arch_attacking = False
            self.arch_attack_finish = False

    def check_shield_cooldown(self):
        if not self.can_shield:
            if (pygame.time.get_ticks() - self.shield_time) > self.shield_cooldown:
                self.can_shield = True
                self.shielding = False

    def check_if_hurt(self):
        if self.just_hurt and not self.sword_attacking and not self.arch_attacking and not self.shielding:
            self.status = 'hit'
            if pygame.time.get_ticks() - self.just_hurt_time > PLAYER_IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def add_experience(self, experience):
        self.ui.add_experience(self.experience, experience)
        self.experience += experience

    def collect_items(self, items):
        for item in items:
            self.equipment.add_item(item)
        print('Dodano itemki')

    def update(self):
        if not self.dead:
            self.movement.get_input()
            self.equipment.update()
            self.get_status()
            self.check_if_hurt()
            self.check_sword_attack_cooldown()
            self.check_arch_attack_cooldown()
            self.check_shield_cooldown()
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

        if self.player.status == 'dead':
            animation_speed = PLAYER_DEATH_ANIMATION_SPEED
        elif self.player.status == 'attack':
            animation_speed = self.player.attack_speed
        else:
            animation_speed = self.animation_speed

        animation = self.animations[self.player.status]

        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            if self.player.status == 'dead':
                self.frame_index = len(animation) - 1
            else:
                self.frame_index = 0
            if self.player.status == 'attack':  # Is that attack animation?
                self.player.status = 'idle'
                self.player.sword_attacking = False
                self.player.sword_hit = True
            if self.player.status == 'arch':  # Is that attack animation?
                self.player.arch_attack_finish = True
                self.player.status = 'idle'
            if self.player.status == 'hit':  # Is that hit animation?
                self.player.status = 'idle'
            if self.player.status == 'shield':  # Is that shield animation?
                self.player.status = 'idle'
                self.player.shielding = False

        image = animation[int(self.frame_index)]

        if self.player.facing_right:
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
        if self.player.can_use_object[0] is True:
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
            draw_text(surface, 'arch_attacking= ' + str(self.player.arch_attacking),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0],
                      self.rect.bottom + SHOW_STATUS_SPACE * 5 - offset[1])
            draw_text(surface, 'sword_hit= ' + str(self.player.sword_hit),
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
        self.on_ceiling = False
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

        if keys[pygame.K_RIGHT] and \
                not self.player.sword_attacking and \
                not self.player.shielding and \
                not self.player.arch_attacking:
            self.direction.x = 1
            self.player.facing_right = True
        elif keys[pygame.K_LEFT] and \
                not self.player.sword_attacking and \
                not self.player.shielding and \
                not self.player.arch_attacking:
            self.direction.x = -1
            self.player.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and \
                self.on_ground and \
                not self.player.just_jumped and \
                not self.player.sword_attacking and \
                not self.player.arch_attacking:
            self.player.movement.jump()
            self.player.just_jumped = True
        if not keys[pygame.K_SPACE]: # Player isn't jumping anymore
            self.player.just_jumped = False
        if keys[pygame.K_ESCAPE]: # Pause game
            self.player.create_pause()
        if keys[pygame.K_d] and \
                not self.player.sword_attacking and \
                not self.player.arch_attacking and \
                not self.player.shielding and \
                not self.player.sword_attacking and \
                self.player.sword_can_attack: # Player attack with sword
            self.player.sword_attack()
        if keys[pygame.K_s] and \
                not self.player.sword_attacking and \
                not self.player.arch_attacking and \
                not self.player.shielding \
                and self.player.can_shield and \
                not self.player.just_hurt: # Player use SHIELD
            self.player.shielding = True
            self.player.can_shield = False
            self.player.shield_time = pygame.time.get_ticks()
        if keys[pygame.K_a] and \
                not self.player.sword_attacking and \
                not self.player.arch_attacking and \
                not self.player.shielding \
                and self.player.arch_can_attack: # Player shot arrow
            self.player.arch_attack()
        if keys[pygame.K_i]: # Show Equipment
            if pygame.time.get_ticks() - self.player.equipment.show_cooldown > 400:
                if self.player.equipment.show:
                    self.player.equipment.show = False
                else: self.player.equipment.show = True
                self.player.equipment.show_cooldown = pygame.time.get_ticks()
        if keys[pygame.K_e]: # Use element:
            if self.player.can_use_object[0]:
                self.player.can_use_object[1].collected = True
                if self.player.can_use_object[1].kind == 'chest':
                    self.player.collect_items(self.player.can_use_object[1].action())

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

