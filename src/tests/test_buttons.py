import pytest
import pygame
from unittest.mock import patch
from buttons import Button


class TestButtons():
    @pytest.fixture()
    def mock_button(self):
        pygame.init()
        pygame.display.set_mode((0, 0))
        button = Button((100, 40), 500, 250, 'text', 'fake_font')
        return button

    @patch('pygame.mouse.get_pos', return_value=(550, 265))
    @patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))
    def test_check_click__is_clicked(self, mock_get_pressed, mock_get_pos, mock_button):
        mock_button.set_image(True)
        action = mock_button.check_click()

        assert action

    @patch('pygame.mouse.get_pos', return_value=(1550, 265))
    @patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))
    def test_check_click__is_not_clicked_1(self, mock_get_pressed, mock_get_pos, mock_button):
        mock_button.set_image(True)
        action = mock_button.check_click()

        assert not action

    @patch('pygame.mouse.get_pos', return_value=(550, 265))
    @patch('pygame.mouse.get_pressed', return_value=(0, 0, 0))
    def test_check_click__is_not_clicked_2(self, mock_get_pressed, mock_get_pos, mock_button):
        mock_button.set_image(True)
        action = mock_button.check_click()

        assert not action