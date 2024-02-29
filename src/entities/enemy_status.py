from pygame.mixer import Sound
from random import choice
from tools.settings import SOUND_SPAWN_VOLUME, SOUND_SPAWN_PATH


class EnemyStatus:
    def __init__(self, kind: str, enemy_id: int) -> None:
        self.type = kind
        self.id = enemy_id
        self.status = 'idle'
        self.facing_right = True
        self.spawned = False
        self.spawn_sound = Sound(SOUND_SPAWN_PATH)
        self.spawn_sound.set_volume(SOUND_SPAWN_VOLUME)

    def set_status(self, new_status: str) -> None:
        self.status = new_status

    def set_facing(self, facing: bool) -> None:
        self.facing_right = facing

    def set_spawned(self) -> None:
        self.spawn_sound.play()
        self.spawned = True

    def reset_status(self) -> None:
        self.status = 'run'
        self.facing_right = choice([True, False])
        self.spawned = False

