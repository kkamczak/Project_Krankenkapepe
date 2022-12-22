import pygame
import sys
from settings import *
from level import Level
from support import draw_text
from overworld import Pause, MainMenu, DeathScene


def print_mask():
    mask = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    mask.fill(GREY)
    mask.set_alpha(150)
    SCREEN.blit(mask, (SCREEN_WIDTH / 2 - mask.get_width() / 2, SCREEN_HEIGHT / 2 - mask.get_height() / 2))


class Game:
    def __init__(self):
        # Overworld creation
        self.main_menu = MainMenu(SCREEN, ['Start', 'Exit'], self.create_level, BUTTON_FONT, self.exit_game, 0)
        self.status = 'main_menu'

        self.level = None
        self.pause = None

        self.paused = False
        self.death_scene = None

        # Sounds:
        self.level_bg_music = pygame.mixer.Sound('content/sounds/background.mp3')
        self.level_bg_music.set_volume(0.03)
        
        self.player_run_music = pygame.mixer.Sound('content/sounds/character/run.ogg')

    def create_level(self):
        self.level = Level(SCREEN, self.create_pause, self.create_main_menu, self.create_death_scene, NORMAL_FONT)
        self.status = 'level'
        self.level_bg_music.play(loops=-1)

    def create_main_menu(self):
        self.main_menu = MainMenu(SCREEN, ['Start', 'Exit'], self.create_level, BUTTON_FONT, self.exit_game, 0)
        self.status = 'main_menu'

    def create_pause(self):
        self.pause = Pause(SCREEN, ['Return', 'Main Menu', 'Exit'], BUTTON_FONT,
                           self.exit_game, self.stop_pause, self.create_main_menu, 0)
        self.status = 'pause'

    def stop_pause(self):
        self.status = 'level'

    def create_death_scene(self):
        self.death_scene = DeathScene(SCREEN, ['Respawn', 'Main Menu', 'Exit'], NORMAL_FONT, DEATH_FONT,
                                      self.create_main_menu, self.create_level, self.exit_game, 70)
        self.status = 'dead'

    def run(self):
        if self.status == 'level':
            self.level.run()
        elif self.status == 'main_menu':
            self.main_menu.run()
        elif self.status == 'pause':
            self.pause.run()
        elif self.status == 'dead':
            if not self.death_scene.end:
                self.level.run()
            self.death_scene.run()

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()


# Pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# Fonts:
NORMAL_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 30)
DEATH_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 70)
FPS_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 30)
BUTTON_FONT = pygame.font.SysFont('content/fonts/ARCADEPI.ttf', 30)

# Start game:
game = Game()

# Game loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.exit_game()

    if game.status == 'main_menu':
        SCREEN.fill(BLACK)
        game.paused = False
    elif game.status == 'level':
        SCREEN.fill(SKY)
        game.paused = False
    elif game.status == 'pause' and not game.paused:
        print_mask()
        game.paused = True
    elif game.status == 'dead':
        SCREEN.fill(SKY)
    #     print_mask()
    #     game.paused = True
    game.run()

    draw_text(SCREEN, 'FPS: ' + str(int(CLOCK.get_fps())), FPS_FONT, GREY, FPS_SHOW_POS[0], FPS_SHOW_POS[1])

    pygame.display.update()
    CLOCK.tick(FPS)
