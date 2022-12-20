import pygame
from math import sin
from settings import PLAYER_MAX_HEALTH, PLAYER_SIZE, PLAYER_SPEED, PLAYER_GRAVITY, PLAYER_JUMP_SPEED, GREY, RED, YELLOW, SWORD_ATTACKING_COOLDOWN, IMMUNITY_FROM_HIT, SCREEN_WIDTH, SHOW_COLLISION_RECTANGLES, SHOW_IMAGE_RECTANGLES, SHIELD_COOLDOWN
from support import import_folder, create_bar
from ui import UI

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, font, create_pause, sword_attack, arch_attack):
        super().__init__()

        self.font = font

        # Player images:
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Player movement:
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.collision_rect = pygame.Rect((self.rect.centerx, self.rect.top - PLAYER_SIZE[0] / 2), PLAYER_SIZE)

        # Player status:
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.just_jumped = False

        # Attacking with Sword:
        self.sword_attacking = False # Is player on sword attack animation?
        self.sword_attack_time = 0 # When did player attack?
        self.sword_attack_cooldown = SWORD_ATTACKING_COOLDOWN # What is cooldown for sword attack?
        self.sword_can_attack = True # Can player attack?
        self.sword_just_attacked = False # Did player just attack? (for not multiple 'D' key pressing)

        # Attacking with Arch
        self.arch_attacking = False
        self.arch_attack_time = 0
        self.arch_attack_cooldown = SWORD_ATTACKING_COOLDOWN
        self.arch_can_attack = True
        self.arch_just_attacked = False

        # Taking hits:
        self.just_hitted = False
        self.just_hitted_time = 0

        # Shielding:
        self.shielding = False
        self.just_shielded = False
        self.can_shield = True
        self.shield_time = 0
        self.shield_cooldown = SHIELD_COOLDOWN

        # Properties:
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health

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

        # Create in-level UI:
        self.ui = UI()


    def import_character_assets(self): # Import all animations:
        character_path = 'content/graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack':[], 'dead':[], 'hit': [], 'shield': [], 'arch': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self): # Animate method

        if self.status == 'dead': animation_speed = 0.15
        else: animation_speed = self.animation_speed

        animation = self.animations[self.status]


        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'dead': self.frame_index = len(animation) - 1
            else: self.frame_index = 0

            if self.status == 'attack': # Is that attack animation?
                self.status = 'idle'
                self.sword_attacking = False
            if self.status == 'arch': # Is that attack animation?
                self.player_arch_attack('player', self.collision_rect, self.facing_right, self.arch_damage, self.arch_can_attack)
                self.arch_can_attack = False
                self.arch_attacking = False
                self.status = 'idle'
            if self.status == 'hit': # Is that hit animation?
                self.status = 'idle'
            if self.status == 'shield': # Is that shield animation?
                self.status = 'idle'
                self.shielding = False


        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
            self.rect.midbottom = self.collision_rect.midbottom
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.midbottom = self.collision_rect.midbottom
            self.rect = self.image.get_rect(midbottom =self.rect.midbottom)
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not self.sword_attacking and not self.shielding and not self.arch_attacking:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] and not self.sword_attacking and not self.shielding and not self.arch_attacking:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground == True and self.just_jumped == False and not self.sword_attacking and not self.arch_attacking:
            self.jump()
            self.just_jumped = True
        if keys[pygame.K_SPACE] == False:
            self.just_jumped = False
        if keys[pygame.K_ESCAPE]:
            self.create_pause()
        if keys[pygame.K_d] and not self.sword_attacking and not self.arch_attacking and not self.shielding and not self.sword_just_attacked and self.sword_can_attack:
            self.sword_attack()
        if keys[pygame.K_d] == False:
            self.sword_just_attacked = False
        if keys[pygame.K_s] and not self.sword_attacking and not self.arch_attacking and not self.shielding and not self.just_shielded and self.can_shield:
            self.shielding = True
            self.just_shielded = True
            self.can_shield = False
            self.shield_time = pygame.time.get_ticks()
        if keys[pygame.K_s] == False:
            self.just_shielded = False
        if keys[pygame.K_a] and not self.sword_attacking and not self.arch_attacking and not self.shielding and not self.arch_just_attacked and self.arch_can_attack:
            self.arch_attack()
        if keys[pygame.K_a] == False:
            self.arch_just_attacked = False


    def get_status(self):
        if self.direction.y < 0 and not self.sword_attacking and not self.shielding:
            if self.status != 'jump': self.frame_index = 0
            self.status = 'jump'
        elif self.direction.y > 1 and not self.sword_attacking and not self.shielding:
            if self.status != 'fall': self.frame_index = 0
            self.status = 'fall'
        elif self.sword_attacking and not self.shielding and not self.arch_attacking:
            if self.status != 'attack': self.frame_index = 0
            self.status = 'attack'
        elif not self.sword_attacking and not self.shielding and self.arch_attacking:
            if self.status != 'arch': self.frame_index = 0
            self.status = 'arch'
        elif not self.sword_attacking and not self.arch_attacking and self.shielding:
            if self.status != 'shield': self.frame_index = 0
            self.status = 'shield'
        else:
            if self.direction.x != 0:
                if self.status != 'run': self.frame_index = 0
                self.status = 'run'
            else:
                if self.status != 'idle': self.frame_index = 0
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def sword_attack(self):
        self.player_sword_attack('player', -1, self.collision_rect, self.facing_right, self.sword_damage, self.sword_can_attack, 40)
        self.sword_attack_time = pygame.time.get_ticks()
        self.sword_attacking = True
        self.sword_just_attacked = True
        self.sword_can_attack = False

    def arch_attack(self):
        self.arch_attack_time = pygame.time.get_ticks()
        self.arch_attacking = True
        self.arch_just_attacked = True


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

    def check_shield_cooldown(self):
        if not self.can_shield:
            if (pygame.time.get_ticks() - self.shield_time) > self.shield_cooldown:
                self.can_shield = True
                self.shielding = False

    def check_if_hitted(self):
        if self.just_hitted and not self.sword_attacking and not self.arch_attacking and not self.shielding:
            self.status = 'hit'
            if pygame.time.get_ticks() - self.just_hitted_time > IMMUNITY_FROM_HIT:
                self.just_hitted = False

    def show_ui(self, screen, offset):

        if not self.dead:
            # Health bar:
            self.ui.show_health(screen, self.max_health, self.health)

            # Sword cooldown:
            if not self.sword_can_attack:
                self.ui.show_attack_cooldown(screen, self.sword_attack_time, self.sword_attack_cooldown, self.collision_rect, offset)

            # Skeletons:
            self.ui.show_skeletons(screen, self.experience, self.font)
            self.ui.update_experience()


    def update(self, screen, offset):
        if not self.dead:
            self.get_input()
            self.get_status()
            self.check_if_hitted()
            self.check_sword_attack_cooldown()
            self.check_arch_attack_cooldown()
            self.check_shield_cooldown()
        self.animate()
        self.show_ui(screen, offset)

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(PLAYER_SIZE)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, self.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)