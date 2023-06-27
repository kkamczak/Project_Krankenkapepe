import pygame
from settings import ENEMY_SCELETON_HEALTH, ENEMY_NINJA_HEALTH, ENEMY_SIZE, GREY, RED, IMMUNITY_FROM_HIT, ENEMY_SPEED, \
    ENEMY_GRAVITY, SHOW_IMAGE_RECTANGLES, SHOW_COLLISION_RECTANGLES, SCELETON_TRIGGER_LENGTH, NINJA_TRIGGER_LENGTH, \
    SHOW_ENEMY_STATUS, WHITE, SMALL_STATUS_FONT, SHOW_STATUS_SPACE
from support import import_folder, draw_text
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_id, pos, kind):
        super().__init__()

        # Select type and id of enemy:
        self.type = kind
        self.id = enemy_id

        # Load  images:
        self.animations = None
        self.import_character_assets()

        # Enemy animation setup:
        self.status = 'run'
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect((self.rect.centerx, self.rect.top - ENEMY_SIZE[0] / 2), ENEMY_SIZE)

        # Variables for movement:
        self.start_position = self.collision_rect.x
        self.past_position = self.collision_rect.x
        self.current_position = self.collision_rect.x
        self.max_position_range = 300
        self.on_right = False
        self.on_left = False

        # Enemy status setup:
        self.facing_right = random.choice([True, False])
        self.on_ground = False
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = ENEMY_SPEED
        self.gravity = ENEMY_GRAVITY

        # Attacking:
        self.combat = False

        # Get hurt:
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

        # Properties:
        self.max_health = 150
        self.health = self.max_health

        # Death:
        self.dead = False
        self.dead_time = 0

        self.stunned = False

    def import_character_assets(self):
        character_path = f'content/graphics/enemies/{self.type}/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                           'stun': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def move(self):
        self.current_position = self.collision_rect.x

        if not self.combat and not self.dead and not self.stunned:
            # Check if actually collided with wall or walked away too far from spawn position:
            if abs(self.current_position - self.start_position) > self.max_position_range:
                if self.facing_right:
                    self.facing_right = False
                else:
                    self.facing_right = True
            if self.facing_right:
                self.direction.x = 1
            else:
                self.direction.x = -1
            if self.on_right:
                self.facing_right = False
                self.on_right = False
            if self.on_left:
                self.facing_right = True
                self.on_left = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def animate(self):
        if self.status != 'attack' and not self.dead:

            if self.just_hurt:
                animation = self.animations['hit']
            elif self.stunned:
                animation = self.animations['stun']
            else:
                animation = self.animations[self.status]

            # Loop over frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
                if self.status == 'stun':
                    self.status = 'run'
                    self.stunned = False
                    self.armor_ratio = 1
                    self.combat_reset()

            image = animation[int(self.frame_index)]

            if self.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom
            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image
                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def animate_dead(self):
        if self.status == 'dead' and self.dead:
            self.direction.x = 0
            self.direction.y = 0
            animation_speed = 0.15

            animation = self.animations['dead']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1

            image = animation[int(self.frame_index)]

            if self.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom

            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def check_if_hurt(self):
        if self.just_hurt:
            if pygame.time.get_ticks() - self.just_hurt_time > IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def combat_reset(self):
        pass

    def draw_health_bar(self, screen, offset):
        if not self.dead:
            hp_max = pygame.Surface((self.collision_rect.width, 5))
            hp_max.fill(GREY)
            cur = pygame.Surface((self.health / self.max_health * self.collision_rect.width, 5))
            cur.fill(RED)

            screen.blit(hp_max, (self.collision_rect.left - offset.x, self.collision_rect.top - 15 - offset.y))
            screen.blit(cur, (self.collision_rect.left - offset.x, self.collision_rect.top - 15 - offset.y))

    def update(self, offset):
        if not self.dead:
            self.check_if_hurt()
            self.animate()
        self.animate_dead()

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(self.collision_rect.size)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, self.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)

        if SHOW_ENEMY_STATUS:
            # Show information for developer
            draw_text(surface, self.type,
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*1 - offset[1])

            draw_text(surface, 'Pos: ' + str(self.rect.center),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*3 - offset[1])

            draw_text(surface, 'Frame index: ' + str(int(self.frame_index)),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx + 5 - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*5 - offset[1])


class Sceleton(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'sceleton')

        # Stats:
        self.max_health = ENEMY_SCELETON_HEALTH
        self.health = self.max_health
        self.damage = 60
        self.experience = 20

        # Sceleton sword attacking:
        self.combat = False
        self.combat_start = 0
        self.preparing = 400
        self.sword_can_attack = True

        # Sceleton sword attack animation:
        self.attack_animation_start = 0
        self.attacking = False

        # Methods:
        self.sword_attack = sword_attack

    def animate_attack(self):
        if self.status == 'attack' and self.attacking and not self.dead:
            animation_speed = 0.3
            animation = self.animations['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > 4:
                self.sword_attack('enemy', self.id, self.collision_rect, self.facing_right, self.damage,
                                  self.sword_can_attack, 80)
                self.sword_can_attack = False

            if self.frame_index >= len(animation):
                self.frame_index = 0
                self.sword_can_attack = True
                self.combat = False
                self.attacking = False
                self.status = 'run'

            image = animation[int(self.frame_index)]

            if self.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom

            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def check_for_combat(self, who):
        player = who
        is_close = abs(self.collision_rect.centerx - player.collision_rect.centerx) < SCELETON_TRIGGER_LENGTH \
                   and abs(self.collision_rect.centery - player.collision_rect.centery) < SCELETON_TRIGGER_LENGTH
        if is_close and not self.combat and not player.dead:
            self.combat = True
            self.combat_start = pygame.time.get_ticks()
            self.status = 'idle'
            self.direction.x = 0

        if is_close and not self.attacking and not player.dead:
            if self.collision_rect.centerx > player.collision_rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

        if abs(self.collision_rect.centerx - player.collision_rect.centerx) > SCELETON_TRIGGER_LENGTH \
                and self.combat and not self.attacking:
            self.combat_reset()

        if self.combat and pygame.time.get_ticks() - self.combat_start > self.preparing and not self.attacking:
            self.sword_can_attack = True
            self.attack()

    def attack(self):
        self.status = 'attack'
        self.attacking = True
        self.frame_index = 0

    def combat_reset(self):
        self.combat = False
        self.sword_can_attack = True
        self.attacking = False
        self.status = 'run'

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.move()


class Ninja(Enemy):
    def __init__(self, enemy_id, pos, arch_attack):
        super().__init__(enemy_id, pos, 'ninja')

        # Stats:
        self.max_health = ENEMY_NINJA_HEALTH
        self.health = self.max_health
        self.damage = 60
        self.experience = 20

        # Attacking:
        self.combat = False
        self.combat_start = 0
        self.preparing = 400
        self.arch_can_attack = True

        # Attack animation:
        self.attack_animation_start = 0
        self.attacking = False

        # Methods:
        self.arch_attack = arch_attack

    def animate_attack(self):
        if self.status == 'attack' and self.attacking and not self.dead:
            animation_speed = 0.15
            animation = self.animations['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > 4:
                self.arch_attack('enemy', self.id, self.collision_rect, self.facing_right, self.damage, self.arch_can_attack)
                self.arch_can_attack = False

            if self.frame_index >= len(animation):
                self.frame_index = 0
                self.arch_can_attack = True
                self.combat = False
                self.attacking = False
                self.status = 'run'

            image = animation[int(self.frame_index)]

            if self.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom

            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def check_for_combat(self, who):
        player = who
        is_close = abs(self.collision_rect.centerx - player.collision_rect.centerx) < NINJA_TRIGGER_LENGTH and abs(
            self.collision_rect.centery - player.collision_rect.centery) < 100
        if is_close and not self.combat and not player.dead:
            self.combat = True
            self.combat_start = pygame.time.get_ticks()
            self.status = 'idle'
            self.direction.x = 0

        if is_close and not self.attacking and not player.dead:
            if self.collision_rect.centerx > player.collision_rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

        if abs(self.collision_rect.centerx - player.collision_rect.centerx) > NINJA_TRIGGER_LENGTH \
                and self.combat and not self.attacking:
            self.combat = False
            self.arch_can_attack = True
            self.attacking = False
            self.status = 'run'

        if self.combat and pygame.time.get_ticks() - self.combat_start > self.preparing and not self.attacking:
            self.arch_can_attack = True
            self.attack()

    def attack(self):
        self.status = 'attack'
        self.attacking = True
        self.frame_index = 0

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.move()
