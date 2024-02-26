from pygame.mixer import Sound
from random import choice


class EnemyStatus:
    def __init__(self, enemy, kind, enemy_id):
        self.enemy = enemy
        self.type = kind
        self.id = enemy_id
        self.status = 'idle'
        self.facing_right = True
        self.spawned = False
        self.spawn_sound = Sound('content/sounds/enemies/spawn.mp3')
        self.spawn_sound.set_volume(0.05)

    def set_status(self, new_status: str) -> None:
        self.status = new_status

    def set_facing(self, facing: bool) -> None:
        self.facing_right = facing

    def set_spawned(self) -> None:
        self.spawn_sound.play()
        self.spawned = True

    def reset_status(self):
        self.status = 'run'
        self.facing_right = choice([True, False])
        self.spawned = False
