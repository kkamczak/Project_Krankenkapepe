from menu.buttons import *
from tools.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE, BUTTONS_SPACE, RED, BUTTON_FONT, DEATH_FONT
from tools.support import draw_text, scale_image


class Overworld:
    def __init__(self, surface, buttons, exit_game, space):

        # Setup
        self.display_surface = surface
        self.wallpaper = pygame.image.load('content/graphics/ui/wallpaper.png').convert_alpha()
        self.wallpaper = scale_image(self.wallpaper, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Buttons:

        self.buttons_sprite = self.setup_buttons(buttons, space)

        # Time to allow clicking
        self.start_time = pygame.time.get_ticks()
        self.allow_click = False
        self.timer_length = 300

        # Button action:
        self.action = ''

        # Methods:
        self.exit_game = exit_game

    @staticmethod
    def setup_buttons(buttons_list, space):
        sprite_group = pygame.sprite.Group()
        button_sprite = None
        x_pos = SCREEN_WIDTH / 2
        y_pos = SCREEN_HEIGHT / 2 - 100
        for button_id, button in enumerate(buttons_list):
            if button == 'Start':
                button_sprite = Start_Button(BUTTON_SIZE, x_pos, y_pos + BUTTONS_SPACE * button_id * 2 + space,
                                             button, BUTTON_FONT)
            if button == 'Return':
                button_sprite = Return_Button(BUTTON_SIZE, x_pos, y_pos + BUTTONS_SPACE * button_id * 2 + space,
                                              button, BUTTON_FONT)
            if button == 'Main Menu':
                button_sprite = Menu_Button(BUTTON_SIZE, x_pos, y_pos + BUTTONS_SPACE * button_id * 2 + space,
                                            button, BUTTON_FONT)
            if button == 'Respawn':
                button_sprite = Respawn(BUTTON_SIZE, x_pos, y_pos + BUTTONS_SPACE * button_id * 2 + space,
                                        button, BUTTON_FONT)
            if button == 'Exit':
                button_sprite = Exit_Button(BUTTON_SIZE, x_pos, y_pos + BUTTONS_SPACE * button_id * 2 + space,
                                            button, BUTTON_FONT)

            sprite_group.add(button_sprite)

        return sprite_group

    def draw_wallpaper(self):
        self.display_surface.blit(self.wallpaper, (0, 0))

    def draw_buttons(self):
        self.buttons_sprite.draw(self.display_surface)
        for button in self.buttons_sprite:
            button.draw_content(self.display_surface)

    def buttons_update(self):
        action = ''
        for button in self.buttons_sprite:
            if button.check_click() and self.allow_click:
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
        self.draw_wallpaper()
        self.draw_buttons()
        self.check_action()


class MainMenu(Overworld):
    def __init__(self, surface, buttons, create_level, exit_game, space):
        super().__init__(surface, buttons, exit_game, space)

        self.create_level = create_level

    def check_action(self):
        super().check_action()
        if self.action == 'Start':
            self.create_level()


class Pause(Overworld):
    def __init__(self, surface, buttons, exit_game, stop_pause, create_main_menu, space):
        super().__init__(surface, buttons, exit_game, space)

        self.pause = True
        self.stop_pause = stop_pause
        self.create_main_menu = create_main_menu

    def check_action(self):
        super().check_action()
        if self.action == 'Main Menu':
            self.create_main_menu()
        if self.action == 'Return':
            self.stop_pause()


class DeathScene(Overworld):
    def __init__(self, surface, buttons, create_main_menu, create_level, exit_game, space):
        super().__init__(surface, buttons, exit_game, space)
        self.text = 'You Died'
        self.alpha = 0
        self.end = False
        self.create_main_menu = create_main_menu
        self.create_level = create_level
        self.image = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))

    def check_action(self):
        super().check_action()
        if self.action == 'Main Menu':
            self.create_main_menu()
        if self.action == 'Respawn':
            self.create_level(respawn=True)

    def run(self):

        draw_text(self.image, self.text, DEATH_FONT, RED, self.image.get_width() / 2,
                  self.image.get_height() / 2 - 100)

        self.image.set_alpha(self.alpha)
        self.display_surface.blit(self.image, (0, 0))

        if self.alpha < 255:
            self.alpha += 2
        else:
            self.click_timer()
            self.draw_buttons()
            self.check_action()
            self.end = True
