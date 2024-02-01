import pygame.math
import pygame.rect
import pytest
from terrain.camera import Camera


class MockPlayerMovement():
    def __init__(self):
        self.collision_rect = pygame.Rect(100, 50, 40, 80)

class TestCamera():
    @pytest.fixture()
    def data(self):
        border_right = 1000
        border_bottom = 1000
        return border_right, border_bottom
    @pytest.fixture()
    def scroll(self):
        screen_size = (1000, 1000)
        player_movement = MockPlayerMovement()
        return screen_size, player_movement

    def test_camera_init__correct_init(self, data):
        camera = Camera(*data)

        assert camera is not None
        assert camera.border['left'] == 0
        assert camera.border['right'] == 1000
        assert camera.border['top'] == 0
        assert camera.border['bottom'] == 1000
        assert isinstance(camera.offset, pygame.math.Vector2)

    def test_scroll_camera__is_scrolling_properly_1(self, data, scroll):
        camera = Camera(*data)
        camera.border['right'] = 2000
        camera.border['bottom'] = 2000
        scroll[1].collision_rect.center = (1000, 1000)
        camera.scroll_camera(*scroll)

        assert camera.offset == (500, 500)

    def test_scroll_camera__is_scrolling_properly_2(self, data, scroll):
        camera = Camera(*data)
        camera.scroll_camera(*scroll)

        assert camera.offset == (0, 0)

    def test_scroll_camera__is_scrolling_properly_3(self, data, scroll):
        camera = Camera(*data)
        scroll[1].collision_rect.center = (1500, 1500)
        camera.scroll_camera(*scroll)

        assert camera.offset == (0, 0)


