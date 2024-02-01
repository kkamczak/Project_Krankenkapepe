import pytest
import pygame
from player.player import Player
from entities.enemies import Sceleton

def mock_function():
    pass

class TestEnemyCombat():
    @pytest.fixture()
    def game(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((0, 0))
        enemy = Sceleton(1, (1010, 80), mock_function)
        player = Player((1000, 50), mock_function, mock_function, mock_function)
        return enemy, player

    def test_check_for_combat__is_preparing_attack(self, game):
        enemy, player = game
        enemy.fighting.check_for_combat(player)

        assert not enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert enemy.fighting.combat['on']
        assert not enemy.fighting.combat['trigger']
        assert enemy.status.status == 'idle'
        assert enemy.movement.direction.x == 0

    def test_check_for_combat__is_only_triggered(self, game):
        enemy, player = game
        enemy.movement.collision_rect.center = (1210, 80)
        player.movement.collision_rect.center = (1010, 80)
        enemy.fighting.check_for_combat(player)

        assert not enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert not enemy.fighting.combat['on']
        assert enemy.fighting.combat['trigger']
        assert enemy.status.status == 'run'

    def test_check_for_combat__is_too_far_to_trigger(self, game):
        enemy, player = game
        enemy.movement.collision_rect.center = (1810, 80)
        player.movement.collision_rect.center = (1010, 80)
        enemy.fighting.check_for_combat(player)

        assert not enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert not enemy.fighting.combat['on']
        assert not enemy.fighting.combat['trigger']

    def test_check_for_combat__do_attack(self, game):
        enemy, player = game
        enemy.fighting.attack['attacking'] = False
        enemy.fighting.attack['able'] = True
        enemy.fighting.combat['on'] = True
        enemy.fighting.combat['trigger'] = True
        enemy.fighting.combat['start'] = pygame.time.get_ticks() - enemy.fighting.combat['preparing'] - 1
        enemy.movement.collision_rect.center = (1050, 80)
        player.movement.collision_rect.center = (1010, 80)

        enemy.fighting.check_for_combat(player)

        assert enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert enemy.fighting.combat['on']
        assert not enemy.fighting.combat['trigger']
        assert enemy.status.status == 'attack'

    def test_check_for_leave_combat_while_triggered(self, game):
        enemy, player = game
        enemy.fighting.attack['attacking'] = False
        enemy.fighting.attack['able'] = True
        enemy.fighting.combat['on'] = False
        enemy.fighting.combat['trigger'] = True
        enemy.movement.collision_rect.center = (1850, 80)
        player.movement.collision_rect.center = (1010, 80)

        enemy.fighting.check_for_combat(player)

        assert not enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert not enemy.fighting.combat['on']
        assert not enemy.fighting.combat['trigger']

    def test_check_for_leave_combat_while_preparing(self, game):
        enemy, player = game
        enemy.fighting.attack['attacking'] = False
        enemy.fighting.attack['able'] = True
        enemy.fighting.combat['on'] = True
        enemy.fighting.combat['trigger'] = True
        enemy.movement.collision_rect.center = (1850, 80)
        player.movement.collision_rect.center = (1010, 80)

        enemy.fighting.check_for_combat(player)

        assert not enemy.fighting.attack['attacking']
        assert enemy.fighting.attack['able']
        assert not enemy.fighting.combat['on']
        assert not enemy.fighting.combat['trigger']
