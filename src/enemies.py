import random
import pygame
from settings import GREY, RED, ENEMY_IMMUNITY_FROM_HIT, ENEMY_SPEED, \
    ENEMY_GRAVITY, SHOW_IMAGE_RECTANGLES, SHOW_COLLISION_RECTANGLES, SHOW_ENEMY_STATUS, WHITE, SMALL_STATUS_FONT, \
    SHOW_STATUS_SPACE, ENEMY_ANIMATIONS_PATH, ENEMY_ANIMATION_SPEED, ENEMY_SIZE, ENEMY_HEALTH, ENEMY_ATTACK_SPEED, \
    ENEMY_TRIGGER_LENGTH, ENEMY_ATTACK_SPACE, ENEMY_ATTACK_RANGE, ENEMY_ULTIMATE_ATTACK_COOLDOWN, ENEMY_DAMAGE, \
    ENEMY_EXPERIENCE, ENEMY_ATTACK_SIZE, SCALE
from support import draw_text, import_character_assets


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_id, pos, kind):
        super().__init__()

        self.status = EnemyStatus(self, kind, enemy_id)
        self.defense = EnemyDefense(self)
        self.properties = EnemyProperties(self)
        self.animations = EnemyAnimations(self)
        self.movement = EnemyMovement(self)
        self.fighting = EnemyFighting(self)

        self.status.reset_status()
        self.properties.reset_properies()
        self.animations.load_animations(pos)
        self.movement.init_movement()

    def update(self):
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

    def set_status(self, new_status: str) -> None:
        self.status = new_status

    def set_facing(self, facing: bool) -> None:
        self.facing_right = facing

    def reset_status(self):
        self.status = 'run'
        self.facing_right = random.choice([True, False])


class EnemyDefense():
    def __init__(self, enemy):
        # Get hurt:
        self.enemy = enemy
        self.just_hurt = False
        self.just_hurt_time = 0
        self.armor_ratio = 1

    def check_if_hurt(self):
        if self.just_hurt:
            if pygame.time.get_ticks() - self.just_hurt_time > ENEMY_IMMUNITY_FROM_HIT:
                self.just_hurt = False

    def kill(self) -> None:
        self.enemy.properties.dead['status'] = True
        self.enemy.properties.dead['time'] = pygame.time.get_ticks()
        self.enemy.animations.frame_index = 0
        self.enemy.movement.direction.x = 0
        self.enemy.status.status = 'dead'

    def hurt(self, damage) -> bool:
        self.just_hurt = True
        self.just_hurt_time = pygame.time.get_ticks()
        self.enemy.properties.health['current'] -= damage * self.armor_ratio
        if self.enemy.properties.health['current'] <= 0:  # Death
            self.kill()
            return True
        return False

    def reset_stun(self):
        self.enemy.status.status = 'run'
        self.enemy.fighting.combat['stunned'] = False
        self.enemy.defense.armor_ratio = 1
        self.enemy.fighting.combat_reset()

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
        type = self.enemy.status.type
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'dead': [], 'hit': [],
                           'stun': []}
        if type == 'dark_knight':
            import_character_assets(
                self.animations, f'{ENEMY_ANIMATIONS_PATH}/{type}/', scale=SCALE * 0.2, flip=True
            )
        else:
            import_character_assets(self.animations, f'{ENEMY_ANIMATIONS_PATH}/{type}/')

        self.frame_index = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED[type]
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
    def animate(self):
        if self.enemy.status.status == 'attack' or self.enemy.properties.dead['status']:
            return
        animation_speed = self.animation_speed
        if self.enemy.defense.just_hurt:
            animation = self.animations['hit']
        elif self.enemy.fighting.combat['stunned']:
            animation = self.animations['stun']
            animation_speed = 0.1
        else:
            animation = self.animations[self.enemy.status.status]

        # Loop over frame index
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.enemy.status.status == 'stun':
                self.enemy.defense.reset_stun()

        image = animation[int(self.frame_index)]
        self.flip_image(image)

    def animate_attack(self):
        if self.enemy.status.status == 'attack' and \
                self.enemy.fighting.attack['attacking'] and \
                not self.enemy.properties.dead['status'] and \
                not self.enemy.fighting.combat['stunned']:
            animation_speed = self.enemy.fighting.attack['speed']
            animation = self.animations['attack']

            # Loop over frame index
            self.frame_index += animation_speed
            if self.frame_index > (len(animation) - 1) and self.enemy.fighting.attack['able']:
                self.enemy.fighting.attack['finish'] = True

            if self.frame_index >= len(animation):
                self.enemy.fighting.reset_attack()

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

            draw_text(surface, 'Combat: ' + str(int(self.enemy.fighting.combat['on'])),
                      SMALL_STATUS_FONT, WHITE, self.rect.centerx + 5 - offset[0], self.rect.bottom + SHOW_STATUS_SPACE*5 - offset[1])

    def draw_health_bar(self, screen, offset):
        if not self.enemy.properties.dead['status']:
            rect = self.enemy.movement.collision_rect
            health = self.enemy.properties.health
            hp_max = pygame.Surface((rect.width, 5))
            hp_max.fill(GREY)
            cur = pygame.Surface(
                (health['current'] / health['max'] * rect.width, 5)
            )
            cur.fill(RED)
            screen.blit(hp_max, (rect.left - offset.x, rect.top - 15 - offset.y))
            screen.blit(cur, (rect.left - offset.x, rect.top - 15 - offset.y))


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

        if not self.enemy.fighting.combat['trigger'] and \
                not self.enemy.fighting.combat['on'] and \
                not self.enemy.properties.dead['status'] and \
                not self.enemy.fighting.combat['stunned']:
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


class EnemyFighting():
    def __init__(self, enemy):
        self.enemy = enemy
        # Attacking:
        self.attack = {
            'speed': ENEMY_ATTACK_SPEED[self.enemy.status.type],
            'damage': ENEMY_DAMAGE[self.enemy.status.type],
            'range': ENEMY_ATTACK_RANGE[self.enemy.status.type],
            'size': ENEMY_ATTACK_SIZE[self.enemy.status.type],
            'space': ENEMY_ATTACK_SPACE[self.enemy.status.type],
            'able': True,
            'attacking': False,
            'start': 0,
            'finish': False
        }
        self.combat = {
            'range': ENEMY_TRIGGER_LENGTH[self.enemy.status.type],
            'trigger': False,
            'on': False,
            'start': 0,
            'preparing': 400,
            'stunned': False
        }

    def check_for_combat(self, player):
        rect = self.enemy.movement.collision_rect
        is_close = abs(rect.centerx - player.movement.collision_rect.centerx) < self.combat['range'] \
                   and abs(rect.centery - player.movement.collision_rect.centery) < self.combat['range']
        is_close_to_attack = abs(rect.centerx - player.movement.collision_rect.centerx) < self.attack['range'] \
                   and abs(rect.centery - player.movement.collision_rect.centery) < self.attack['range']
        if is_close_to_attack and not self.combat['on'] and not player.properties.dead['status']:
            self.combat['on'] = True
            self.combat['start'] = pygame.time.get_ticks()
            self.enemy.status.status = 'idle'
            self.enemy.movement.direction.x = 0
            if rect.centerx > player.movement.collision_rect.centerx:
                self.enemy.status.facing_right = False
            else:
                self.enemy.status.facing_right = True

        if is_close and not is_close_to_attack and not self.attack['attacking'] and not player.properties.dead['status']:
            self.combat['trigger'] = True
            if rect.centerx > player.movement.collision_rect.centerx:
                self.enemy.status.facing_right = False
                self.enemy.movement.direction.x = -1
            else:
                self.enemy.status.facing_right = True
                self.enemy.movement.direction.x = 1
        else:
            self.combat['trigger'] = False

        if abs(rect.centerx - player.movement.collision_rect.centerx) > self.combat['range'] \
                and self.combat['on'] and not self.attack['attacking']:
            self.combat_reset()

        if self.combat['on'] and \
                pygame.time.get_ticks() - self.combat['start'] > self.combat['preparing'] and \
                not self.attack['attacking'] and \
                abs(rect.centerx - player.movement.collision_rect.centerx) < self.attack['range']:
            self.attack['able'] = True
            self.do_attack(player.movement.collision_rect)

    def combat_reset(self):
        self.attack['attacking'] = False
        self.attack['able'] = True
        self.combat['on'] = False
        self.combat['trigger'] = False
        self.enemy.status.status = 'run'

    def do_attack(self, player_pos):
        self.enemy.status.status = 'attack'
        self.attack['attacking'] = True
        self.enemy.animations.frame_index = 0

    def reset_attack(self):
        self.enemy.animations.frame_index = 0
        self.attack['able'] = True
        self.combat['on'] = False
        self.attack['attacking'] = False
        self.enemy.status.status = 'run'


class EnemyFightingThunder(EnemyFighting):
    def __init__(self, enemy):
        super().__init__(enemy)

    def do_attack(self, player_pos):
        super().do_attack(player_pos)
        if pygame.time.get_ticks() - self.enemy.thunder['time'] > self.enemy.thunder['cooldown']:
            self.enemy.thunder_attack(
                'enemy', self.enemy.status.id, player_pos,
                self.enemy.fighting.attack['damage'] * 10, self.enemy.fighting.attack['able']
            )
            self.enemy.thunder['time'] = pygame.time.get_ticks()

class Sceleton(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'sceleton')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.sword_attack(self)
            self.fighting.attack['able'] = False
            self.fighting.attack['finish'] = False

    def update(self):
        super().update()
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
        if self.fighting.attack['finish']:
            self.arch_attack('arrow', self)
            self.fighting.attack['able'] = False
            self.fighting.attack['finish'] = False

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class Wizard(Enemy):
    def __init__(self, enemy_id, pos, arch_attack, thunder_attack):
        super().__init__(enemy_id, pos, 'wizard')
        self.thunder = {
            'time': pygame.time.get_ticks(),
            'cooldown': ENEMY_ULTIMATE_ATTACK_COOLDOWN[self.status.type]
        }
        # Methods:
        self.arch_attack = arch_attack
        self.thunder_attack = thunder_attack

        self.fighting = EnemyFightingThunder(self)

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.arch_attack('death_bullet', self)
            self.fighting.attack['able'] = False
            self.fighting.attack['finish'] = False

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()


class DarkKnight(Enemy):
    def __init__(self, enemy_id, pos, sword_attack):
        super().__init__(enemy_id, pos, 'dark_knight')

        # Methods:
        self.sword_attack = sword_attack

    def check_attack_finish(self):
        if self.fighting.attack['finish']:
            self.sword_attack(self)
            self.fighting.attack['able'] = False
            self.fighting.attack['finish'] = False

    def update(self):
        super().update()
        if not self.properties.dead['status']:
            self.animations.animate_attack()
            self.check_attack_finish()
            self.movement.move()
