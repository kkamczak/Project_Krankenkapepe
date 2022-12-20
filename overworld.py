import pygame
from game_data import levels
from buttons import *
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE, BUTTONS_SPACE, RED
from support import draw_text


class Overworld:
    def __init__(self, surface, buttons, font, exit_game, space):

        # Setup
        self.display_surface = surface

        # Buttons:

        self.buttons_sprite = self.setup_buttons(buttons, font, space)

        # Time to allow clicking
        self.start_time = pygame.time.get_ticks()
        self.allow_click = False
        self.timer_length = 300

        # Button action:
        self.action = ''

        # Methods:
        self.exit_game = exit_game

    def setup_buttons(self, list, font, space):
        sprite_group = pygame.sprite.Group()
        for id, button in enumerate(list):
            if button == 'Start':
                button_sprite = Start_Button(BUTTON_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 + BUTTONS_SPACE * id * 2 + space, button, font)
            if button == 'Return':
                button_sprite = Return_Button(BUTTON_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 + BUTTONS_SPACE * id * 2 + space, button, font)
            if button == 'Main Menu':
                button_sprite = Menu_Button(BUTTON_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 + BUTTONS_SPACE * id * 2 + space, button, font)
            if button == 'Respawn':
                button_sprite = Respawn(BUTTON_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 + BUTTONS_SPACE * id * 2 + space, button, font)
            if button == 'Exit':
                button_sprite = Exit_Button(BUTTON_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 + BUTTONS_SPACE * id * 2 + space, button, font)

            sprite_group.add(button_sprite)

        return sprite_group

    def draw_buttons(self):
        self.buttons_sprite.draw(self.display_surface)
        for button in self.buttons_sprite:
            button.draw_content(self.display_surface)

    def buttons_update(self):
        action = ''
        for button in self.buttons_sprite:
            if button.check_click() and self.allow_click == True:
                action = button.type
                break

        return action

    def click_timer(self):
        if not self.allow_click:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_click = True

    def check_action(self):
        self.action = self.buttons_update()
        if self.action == 'Exit':
            self.exit_game()

    def run(self):
        self.click_timer()
        self.draw_buttons()
        self.check_action()


class Main_Menu(Overworld):
    def __init__(self, surface, buttons, create_level, font, exit_game, space):
        super().__init__(surface, buttons, font, exit_game, space)

        self.create_level = create_level

    def check_action(self):
        super().check_action()
        if self.action == 'Start':
            self.create_level()


class Pause(Overworld):
    def __init__(self, surface, buttons, font, exit_game, stop_pause, create_main_menu, space):
        super().__init__(surface, buttons, font, exit_game, space)

        self.pause = True
        self.stop_pause = stop_pause
        self.create_main_menu = create_main_menu

    def check_action(self):
        super().check_action()
        if self.action == 'Main Menu':
            self.create_main_menu()
        if self.action == 'Return':
            self.stop_pause()

class Death_Scene(Overworld):
    def __init__(self, surface, buttons, font, death_font, create_main_menu, create_level, exit_game, space):
        super().__init__(surface, buttons, font, exit_game, space)
        self.text = 'You Died'
        self.alpha = 0
        self.end = False
        self.create_main_menu = create_main_menu
        self.create_level = create_level
        self.death_font = death_font
        self.image = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))

    def check_action(self):
        super().check_action()
        if self.action == 'Main Menu':
            self.create_main_menu()
        if self.action == 'Respawn':
            self.create_level()

    def run(self):

        draw_text(self.image, self.text, self.death_font, RED, self.image.get_width() / 2, self.image.get_height() / 2 - 100)

        self.image.set_alpha(self.alpha)
        self.display_surface.blit(self.image, (0, 0))

        if self.alpha < 255:
            self.alpha += 2
        else:
            self.click_timer()
            self.draw_buttons()
            self.check_action()
            self.end = True



