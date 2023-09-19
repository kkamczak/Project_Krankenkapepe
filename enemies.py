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
        self.defense = EnemyDefense()
        self.properties = EnemyProperties(self)
        self.animations = EnemyAnimations(self)
        self.movement = EnemyMovement(self)

        self.status.reset_status()
        self.properties.reset_properies()
        self.animations.load_animations(pos)
        self.movement.init_movement()

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

        self.damage = ENEMY_DAMAGE[self.status.type]

        self.stunned = False

    def check_for_combat(self, player):
        is_close = abs(self.movement.collision_rect.centerx - player.movement.collision_rect.centerx) < self.trigger_length \
                   and abs(self.movement.collision_rect.centery - player.movement.collision_rect.centery) < self.trigger_length
        is_close_to_attack = abs(self.movement.collision_rect.centerx - player.movement.collision_rect.centerx) < self.attack_range \
                   and abs(self.movement.collision_rect.centery - player.movement.collision_rect.centery) < self.attack_range
        if is_close_to_attack and not self.combat and not player.properties.dead['status']:
            self.combat = True
            self.combat_start = pygame.time.get_ticks()
            self.status.status = 'idle'
            self.movement.direction.x = 0
            if self.movement.collision_rect.centerx > player.movement.collision_rect.centerx:
                self.status.facing_right = False
            else:
                self.status.facing_right = True

        if is_close and not is_close_to_attack and not self.attacking and not player.properties.dead['status']:
            self.trigger = True
            if self.movement.collision_rect.centerx > player.movement.collision_rect.centerx:
                self.status.facing_right = False
                self.movement.direction.x = -1
            else:
                self.status.facing_right = True
                self.movement.direction.x = 1
        else:
            self.trigger = False

        if abs(self.movement.collision_rect.centerx - player.movement.collision_rect.centerx) > self.trigger_length \
                and self.combat and not self.attacking:
            self.combat_reset()

        if self.combat and pygame.time.get_ticks() - self.combat_start > self.preparing and not self.attacking \
                and abs(self.movement.collision_rect.centerx - player.movement.collision_rect.centerx) < self.attack_range:
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
        if not self.properties.dead['status']:
            hp_max = pygame.Surface((self.movement.collision_rect.width, 5))
            hp_max.fill(GREY)
            cur = pygame.Surface((self.properties.health['current'] / self.properties.health['max'] * self.movement.collision_rect.width, 5))
            cur.fill(RED)

            screen.blit(hp_max, (self.movement.collision_rect.left - offset.x, self.movement.collision_rect.top - 15 - offset.y))
            screen.blit(cur, (self.movement.collision_rect.left - offset.x, self.movement.collision_rect.top - 15 - offset.y))

    def update(self, offset):
        if not self.properties.dead['status']:
            self.defense.check_if_hurt()
            self.animations.animate()
        self.animations.animate_dead()


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


class EnemyDefense():
    def __init__(self):
        # Get hurt:
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

    def check_if_hurt(self):
        if self.just_hurt:
            if pygame.time.get_ticks() - self.just_hurt_time > ENEMY_IMMUNITY_FROM_HIT:
                self.just_hurt = False


class EnemyProperties():
    def __init__(self, enemy):
        self.enemy = enemy
        self.health = {
            'current': ENEMY_HEALTH[self.enemy.status.type],
            'max': ENEMY_HEALTH[self.enemy.status.type]
        }
        self.experience = {
            'current': ENEMY_EXPERIENCE[self.enemy.status.type]
        }
        self.dead = {
            'status': False,
            'time': 0
        }
    def reset_properies(self):
        self.health = {
            'current': ENEMY_HEALTH[self.enemy.status.type],
            'max': ENEMY_HEALTH[self.enemy.status.type]
        }
        self.experience = {
            'current': ENEMY_EXPERIENCE[self.enemy.status.type]
        }


class EnemyAnimations():
    def __init__(self, enemy):
        self.enemy = enemy
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0
        self.image = None
        self.rect = None

    def load_animations(self, position):
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                           'stun': []}
        if self.enemy.status.type == 'dark_knight':
            import_character_assets(self.animations, f'{ENEMY_ANIMATIONS_PATH}/{self.enemy.status.type}/', scale=SCALE * 0.2,
                                    flip=True)
        else:
            import_character_assets(self.animations, f'{ENEMY_ANIMATIONS_PATH}/{self.enemy.status.type}/')

        self.frame_index = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED[self.enemy.status.type]
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
    def animate(self):
        if self.enemy.status.status == 'attack' or self.enemy.properties.dead['status']:
            return
        animation_speed = self.animation_speed
        if self.enemy.defense.just_hurt:
            animation = self.animations['hit']
        elif self.enemy.stunned:
            animation = self.animations['stun']
            animation_speed = 0.1
        else:
            animation = self.animations[self.enemy.status.status]

        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.enemy.status.status == 'stun':
                self.enemy.status.status = 'run'
                self.enemy.stunned = False
                self.enemy.defense.armor_ratio = 1
                self.enemy.combat_reset()

        image = animation[int(self.frame_index)]
        self.flip_image(image)

    def animate_attack(self):
        if self.enemy.status.status == 'attack' and \
                self.enemy.attacking and \
                not self.enemy.properties.dead['status'] and \
                not self.enemy.stunned:
            animation_speed = self.enemy.attack_speed
            animation = self.animations['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > (len(animation) - 1) and self.enemy.can_attack:
                self.enemy.attack_finish = True

            if self.frame_index >= len(animation):
                self.frame_index = 0
                self.enemy.can_attack = True
                self.enemy.combat = False
                self.enemy.attacking = False
                self.enemy.status.status = 'run'

            image = animation[int(self.frame_index)]
            self.flip_image(image)

    def animate_dead(self):
        if self.enemy.status.status == 'dead' and self.enemy.properties.dead['status']:
            self.enemy.movement.direction.x = 0
            self.enemy.movement.direction.y = 0
            animation_speed = 0.15

            animation = self.animations['dead']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1

            image = animation[int(self.frame_index)]
            self.flip_image(image)

    def flip_image(self, image):
        if self.enemy.status.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        self.rect.midbottom = self.enemy.movement.collision_rect.midbottom
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

        # Show collision rectangles:
        if SHOW_COLLISION_RECTANGLES:
            collide_surface = pygame.Surface(self.enemy.movement.collision_rect.size)
            collide_surface.set_alpha(40)
            surface.blit(collide_surface, self.enemy.movement.collision_rect.topleft - offset)

        # Show image rectangles:
        if SHOW_IMAGE_RECTANGLES:
            image_surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            image_surface.set_alpha(30)
            surface.blit(image_surface, self.rect.topleft - offset)

        if SHOW_ENEMY_STATUS:
            # Show information for developer
            draw_text(surface, self.enemy.status.type,
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*1 - offset[1])

            draw_text(surface, 'Pos: ' + str(self.rect.center),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*3 - offset[1])

            draw_text(surface, 'Combat: ' + str(int(self.enemy.combat)),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx + 5 - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*5 - offset[1])


class EnemyMovement():
    def __init__(self, enemy):
        self.enemy = enemy

        self.collision_rect = None
        self.position = None

        self.on_right = False
        self.on_left = False
        self.on_ground = False

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = ENEMY_SPEED[self.enemy.status.type]
        self.gravity = ENEMY_GRAVITY

    def init_movement(self):
        self.collision_rect = pygame.Rect(
            (self.enemy.animations.rect.centerx,
             self.enemy.animations.rect.top - int(ENEMY_SIZE[self.enemy.status.type][1] / 2)),
            ENEMY_SIZE[self.enemy.status.type]
        )
        self.position = {
            'start': self.collision_rect.x,
            'past': self.collision_rect.x,
            'current': self.collision_rect.x,
            'max': 300
        }

    def move(self):
        self.position['current'] = self.collision_rect.x

        if not self.enemy.trigger and \
                not self.enemy.combat and \
                not self.enemy.properties.dead['status'] and \
                not self.enemy.stunned:
            # Check if actually collided with wall or walked away too far from spawn position:
            delta = self.position['current'] - self.position['start']
            if abs(self.position['current'] - self.position['start']) > self.position['max']:
                if self.enemy.status.facing_right and delta > 0:
                    self.enemy.status.facing_right = False
                elif not self.enemy.status.facing_right and delta < 0:
                    self.enemy.status.facing_right = True
            if self.enemy.status.facing_right:
                self.direction.x = 1
            else:
                self.direction.x = -1
            if self.on_right:
                self.enemy.status.facing_right = False
                self.on_right = False
            if self.on_left:
                self.enemy.status.facing_right = True
                self.on_left = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

class Sceleton(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'sceleton')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.sword_attack(self.status.type, self.status.id, self.movement.collision_rect, self.status.facing_right, self.damage,
                              self.can_attack, self.attack_space, ENEMY_ATTACK_SIZE[self.status.type][1])
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class Ninja(Enemy):
    def __init__(self, enemy_id, pos, arch_attack):
        super().__init__(enemy_id, pos, 'ninja')

        # Methods:
        self.arch_attack = arch_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.arch_attack('arrow', self.status.type, self.status.id, self.movement.collision_rect, self.status.facing_right, self.damage, self.can_attack)
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


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
            self.arch_attack('death_bullet', self.status.type, self.status.id, self.movement.collision_rect, self.status.facing_right, self.damage, self.can_attack)
            self.can_attack = False
            self.attack_finish = False

    def attack(self, player_pos):
        super().attack(player_pos)
        if pygame.time.get_ticks() - self.thunder_attack_time > self.cooldown:
            self.thunder_attack('enemy', self.status.id, player_pos, 1000, self.can_attack)
            self.thunder_attack_time = pygame.time.get_ticks()

    def update(self, offset):
        super().update(offset)
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()



class Dark_Knight(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'dark_knight')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.attack_finish:
            self.sword_attack(self.status.type, self.status.id, self.movement.collision_rect, self.status.facing_right, self.damage,
                              self.can_attack, self.attack_space, ENEMY_ATTACK_SIZE[self.status.type][1])
            self.can_attack = False
            self.attack_finish = False

    def update(self, offset):
        super().update(offset)
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()
