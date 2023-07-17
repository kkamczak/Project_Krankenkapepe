import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GREY, BLACK, WHITE, SKY, FPS, FPS_FONT, FPS_SHOW_POS, SOUND_PLAY_MUSIC, BIG_FONT
from level import Level
from support import draw_text
from overworld import Pause, MainMenu, DeathScene


def print_mask():
    mask = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    mask.fill(GREY)
    mask.set_alpha(150)
    SCREEN.blit(mask, (SCREEN_WIDTH / 2 - mask.get_width() / 2, SCREEN_HEIGHT / 2 - mask.get_height() / 2))


class Game:
    def __init__(self) -> None:
        # Overworld creation
        self.main_menu: object = MainMenu(SCREEN, ['Start', 'Exit'], self.create_level, self.exit_game, 0)
        self.status: str = 'main_menu'

        self.level: object = None
        self.pause: object = None

        self.paused: bool = False
        self.death_scene: object = None

        # Sounds:
        self.level_bg_music = pygame.mixer.Sound('content/sounds/background.mp3')
        self.level_bg_music.set_volume(0.03)

    def create_level(self) -> None:
        SCREEN.fill(BLACK)
        draw_text(SCREEN, 'Loading...', BIG_FONT, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.level = Level(SCREEN, self.create_pause, self.create_main_menu, self.create_death_scene)
        self.status = 'level'
        if SOUND_PLAY_MUSIC: self.level_bg_music.play(loops=-1)

    def create_main_menu(self) -> None:
        self.main_menu = MainMenu(SCREEN, ['Start', 'Exit'], self.create_level, self.exit_game, 0)
        self.status = 'main_menu'

    def create_pause(self) -> None:
        self.pause = Pause(SCREEN, ['Return', 'Main Menu', 'Exit'], self.exit_game, self.stop_pause, self.create_main_menu, 0)
        self.status = 'pause'

    def stop_pause(self) -> None:
        self.status = 'level'

    def create_death_scene(self) -> None:
        self.death_scene = DeathScene(SCREEN, ['Respawn', 'Main Menu', 'Exit'], self.create_main_menu, self.create_level, self.exit_game, 70)
        self.status = 'dead'

    def run_loop(self) -> None:
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
    def exit_game() -> None:
        pygame.quit()
        sys.exit()

    @staticmethod
    def show_fps() -> None:
        draw_text(SCREEN, 'FPS: ' + str(int(CLOCK.get_fps())), FPS_FONT, GREY, FPS_SHOW_POS[0], FPS_SHOW_POS[1])


# Pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

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

    game.run_loop()

    game.show_fps()

    pygame.display.update()

    CLOCK.tick(FPS)
