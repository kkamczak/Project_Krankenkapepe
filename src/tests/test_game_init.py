import pytest
import pygame
from game import Game


class TestGameInit():
    @pytest.fixture()
    def main(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((0, 0))
        CLOCK = pygame.time.Clock()
        game = Game(SCREEN, CLOCK)
        return game

    def test_game_init__correct_start_overworld(self, main):
        game = main
        assert game.status == 'main_menu'
        assert game.main_menu is not None
        assert game.level is None
        assert game.pause is None
        assert game.death_scene is None
        assert not game.paused

    def test_game_init__create_level(self, main):
        game = main
        game.create_level()
        assert game.status == 'level'
        assert game.level is not None
        assert not game.paused

    def test_game_init__create_main_menu(self, main):
        game = main
        game.create_main_menu()
        assert game.status == 'main_menu'
        assert game.main_menu is not None
        assert not game.paused

    def test_game_init__create_pause(self, main):
        game = main
        game.create_pause()
        assert game.status == 'pause'
        assert game.pause is not None
        assert not game.paused

    def test_game_init__stop_pause(self, main):
        game = main
        game.create_pause()
        assert game.status == 'pause'
        assert game.pause is not None
        assert not game.paused

    def test_game_init__create_death_scene(self, main):
        game = main
        game.create_death_scene()
        assert game.status == 'dead'
        assert game.death_scene is not None
        assert not game.paused

