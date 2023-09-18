import pygame
from settings import GREY, RED, ENEMY_IMMUNITY_FROM_HIT, ENEMY_SPEED, \
    ENEMY_GRAVITY, SHOW_IMAGE_RECTANGLES, SHOW_COLLISION_RECTANGLES, SHOW_ENEMY_STATUS, WHITE, SMALL_STATUS_FONT, \
    SHOW_STATUS_SPACE, ENEMY_ANIMATIONS_PATH, ENEMY_ANIMATION_SPEED, ENEMY_SIZE, ENEMY_HEALTH, ENEMY_ATTACK_SPEED, \
    ENEMY_TRIGGER_LENGTH, ENEMY_ATTACK_SPACE, ENEMY_ATTACK_RANGE, ENEMY_ULTIMATE_ATTACK_COOLDOWN, ENEMY_DAMAGE, \
    ENEMY_EXPERIENCE, ENEMY_ATTACK_SIZE, TILE_SIZE, SCALE
from support import draw_text, import_character_assets
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_id, pos, kind):
        super().__init__()

        self.status = EnemyStatus(self, kind, enemy_id)
        self.status.reset_status()

        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                           'stun': []}
        if self.status.type == 'dark_knight':
            import_character_assets(self.animations, f'{ENEMY_ANIMATIONS_PATH}/{self.status.type}/', scale=SCALE*0.2, flip=True)
        else:
            import_character_assets(self.animations, f'{ENEMY_ANIMATIONS_PATH}/{self.status.type}/')

        # Enemy animation setup:
        self.frame_index = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED[self.status.type]
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect((self.rect.centerx, self.rect.top - ENEMY_SIZE[self.status.type][1] / 2), ENEMY_SIZE[self.status.type])

        # Variables for movement:
        self.start_position = self.collision_rect.x
        self.past_position = self.collision_rect.x
        self.current_position = self.collision_rect.x
        self.max_position_range = 300
        self.on_right = False
        self.on_left = False

        # Enemy status setup:
        self.on_ground = False
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = ENEMY_SPEED[self.status.type]
        self.gravity = ENEMY_GRAVITY

        # Attacking:
        self.attack_speed = ENEMY_ATTACK_SPEED[self.status.type]
        self.trigger_length = ENEMY_TRIGGER_LENGTH[self.status.type]
        self.attack_range = ENEMY_ATTACK_RANGE[self.status.type]
        self.attack_space = ENEMY_ATTACK_SPACE[self.status.type]
        self.trigger = False
        self.combat = False
        self.combat_start = 0
        self.preparing = 400
        self.can_attack = True
        self.attack_finish = False

        # Attack animation:
        self.attack_animation_start = 0
        self.attacking = False

        # Get hurt:
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

        # Properties:
        self.max_health = ENEMY_HEALTH[self.status.type]
        self.health = self.max_health
        self.damage = ENEMY_DAMAGE[self.status.type]
        self.experience = ENEMY_EXPERIENCE[self.status.type]

        # Death:
        self.dead = False
        self.dead_time = 0

        self.stunned = False

    def move(self):
        self.current_position = self.collision_rect.x

        if not self.trigger and not self.combat and not self.dead and not self.stunned:
            # Check if actually collided with wall or walked away too far from spawn position:
            delta = self.current_position - self.start_position
            if abs(self.current_position - self.start_position) > self.max_position_range:
                if self.status.facing_right and delta > 0:
                    self.status.facing_right = False
                elif not self.status.facing_right and delta < 0:
                    self.status.facing_right = True
            if self.status.facing_right:
                self.direction.x = 1
            else:
                self.direction.x = -1
            if self.on_right:
                self.status.facing_right = False
                self.on_right = False
            if self.on_left:
                self.status.facing_right = True
                self.on_left = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def animate(self):
        if self.status.status != 'attack' and not self.dead:
            animation_speed = self.animation_speed
            if self.just_hurt:
                animation = self.animations['hit']
            elif self.stunned:
                animation = self.animations['stun']
                animation_speed = 0.1

            else:
                animation = self.animations[self.status.status]

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
                if self.status.status == 'stun':
                    self.status.status = 'run'
                    self.stunned = False
                    self.armor_ratio = 1
                    self.combat_reset()

            image = animation[int(self.frame_index)]

            if self.status.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom
            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image
                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    def animate_attack(self):
        if self.status.status == 'attack' and self.attacking and not self.dead and not self.stunned:
            animation_speed = self.attack_speed
            animation = self.animations['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > (len(animation)-1) and self.can_attack:
                self.attack_finish = True

            if self.frame_index >= len(animation):
                self.frame_index = 0
                self.can_attack = True
                self.combat = False
                self.attacking = False
                self.status.status = 'run'

            image = animation[int(self.frame_index)]

            if self.status.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom

            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    def animate_dead(self):
        if self.status.status == 'dead' and self.dead:
            self.direction.x = 0
            self.direction.y = 0
            animation_speed = 0.15

            animation = self.animations['dead']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1

            image = animation[int(self.frame_index)]

            if self.status.facing_right:
                self.image = image
                self.rect.midbottom = self.collision_rect.midbottom

            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

                self.rect.midbottom = self.collision_rect.midbottom

            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def check_if_hurt(self):
        if self.just_hurt:
            if pygame.time.get_ticks() - self.just_hurt_time > ENEMY_IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def check_for_combat(self, who):
        player = who
        is_close = abs(self.collision_rect.centerx - player.movement.collision_rect.centerx) < self.trigger_length \
                   and abs(self.collision_rect.centery - player.movement.collision_rect.centery) < self.trigger_length
        is_close_to_attack = abs(self.collision_rect.centerx - player.movement.collision_rect.centerx) < self.attack_range \
                   and abs(self.collision_rect.centery - player.movement.collision_rect.centery) < self.attack_range
        if is_close_to_attack and not self.combat and not player.dead:
            self.combat = True
            self.combat_start = pygame.time.get_ticks()
            self.status.status = 'idle'
            self.direction.x = 0
            if self.collision_rect.centerx > player.movement.collision_rect.centerx:
                self.status.facing_right = False
            else:
                self.status.facing_right = True



        if is_close and not is_close_to_attack and not self.attacking and not player.dead:
            self.trigger = True
            if self.collision_rect.centerx > player.movement.collision_rect.centerx:
                self.status.facing_right = False
                self.direction.x = -1
            else:
                self.status.facing_right = True
                self.direction.x = 1
        else:
            self.trigger = False

        if abs(self.collision_rect.centerx - player.movement.collision_rect.centerx) > self.trigger_length \
                and self.combat and not self.attacking:
            self.combat_reset()

        if self.combat and pygame.time.get_ticks() - self.combat_start > self.preparing and not self.attacking \
                and abs(self.collision_rect.centerx - player.movement.collision_rect.centerx) < self.attack_range:
            self.can_attack = True
            self.attack(player.movement.collision_rect)

    def combat_reset(self):
        self.trigger = False
        self.combat = False
        self.can_attack = True
        self.attacking = False
        self.status.status = 'run'

    def attack(self, player_pos):
        self.status.status = 'attack'
        self.attacking = True
        self.frame_index = 0

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
            draw_text(surface, self.status.type,
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*1 - offset[1])

            draw_text(surface, 'Pos: ' + str(self.rect.center),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*3 - offset[1])

            draw_text(surface, 'Combat: ' + str(int(self.combat)),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx + 5 - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*5 - offset[1])

class EnemyStatus():
    def __init__(self, enemy, kind, enemy_id):
        self.enemy = enemy
        self.type = kind
        self.id = enemy_id
        self.status = 'idle'
        self.facing_right = True

    def reset_status(self):
        self.status = 'run'
        self.facing_right = random.choice([True, False])

class Sceleton(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'sceleton')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.sword_attack(self.status.type, self.status.id, self.collision_rect, self.status.facing_right, self.damage,
                              self.can_attack, self.attack_space, ENEMY_ATTACK_SIZE[self.status.type][1])
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.check_attack_finish()
            self.move()


class Ninja(Enemy):
    def __init__(self, enemy_id, pos, arch_attack):
        super().__init__(enemy_id, pos, 'ninja')

        # Methods:
        self.arch_attack = arch_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.arch_attack('arrow', self.status.type, self.status.id, self.collision_rect, self.status.facing_right, self.damage, self.can_attack)
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.check_attack_finish()
            self.move()


class Wizard(Enemy):
    def __init__(self, enemy_id, pos, arch_attack, thunder_attack):
        super().__init__(enemy_id, pos, 'wizard')

        self.thunder_attack_time = pygame.time.get_ticks()

        # Methods:
        self.arch_attack = arch_attack
        self.thunder_attack = thunder_attack
        self.cooldown = ENEMY_ULTIMATE_ATTACK_COOLDOWN[self.status.type]
    def check_attack_finish(self):
        if self.attack_finish:
            self.arch_attack('death_bullet', self.status.type, self.status.id, self.collision_rect, self.status.facing_right, self.damage, self.can_attack)
            self.can_attack = False
            self.attack_finish = False

    def attack(self, player_pos):
        super().attack(player_pos)
        if pygame.time.get_ticks() - self.thunder_attack_time > self.cooldown:
            self.thunder_attack('enemy', self.status.id, player_pos, 1000, self.can_attack)
            self.thunder_attack_time = pygame.time.get_ticks()

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.check_attack_finish()
            self.move()



class Dark_Knight(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'dark_knight')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.sword_attack(self.status.type, self.status.id, self.collision_rect, self.status.facing_right, self.damage,
                              self.can_attack, self.attack_space, ENEMY_ATTACK_SIZE[self.status.type][1])
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.dead:
            self.animate_attack()
            self.check_attack_finish()
            self.move()
