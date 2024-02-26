from pygame import Vector2, Rect
from tools.settings import ENEMY_SPEED, ENEMY_GRAVITY, ENEMY_SIZE


class EnemyMovement:
    def __init__(self, enemy):
        self.enemy = enemy

        self.collision_rect = None
        self.position = None

        self.on_right = False
        self.on_left = False
        self.on_ground = False

        self.direction = Vector2(0, 0)
        self.speed = ENEMY_SPEED[self.enemy.status.type]
        self.gravity = ENEMY_GRAVITY

    def set_collision_rect(self, new_rect: Rect) -> None:
        self.collision_rect = new_rect

    def set_position(self, key: str, value: int) -> None:
        self.position[key] = value

    def set_jump_speed(self, new_speed: float) -> None:
        self.jump_speed = new_speed

    def set_on_right(self, new_value: bool) -> None:
        self.on_right = new_value

    def set_on_left(self, new_value: bool) -> None:
        self.on_left = new_value

    def set_on_ground(self, new_value: bool) -> None:
        self.on_ground = new_value

    def set_direction(self, new_direction: Vector2) -> None:
        self.direction = new_direction

    def set_speed(self, new_speed: int) -> None:
        self.speed = new_speed

    def set_gravity(self, new_gravity: float) -> None:
        self.gravity = new_gravity

    def init_movement(self):
        self.collision_rect = Rect(
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
                    self.enemy.status.set_facing(False)
                elif not self.enemy.status.facing_right and delta < 0:
                    self.enemy.status.set_facing(True)
            if self.enemy.status.facing_right:
                self.direction.x = 1
            else:
                self.direction.x = -1
            if self.on_right:
                self.enemy.status.set_facing(False)
                self.on_right = False
            if self.on_left:
                self.enemy.status.set_facing(True)
                self.on_left = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y
