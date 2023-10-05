import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GREY, BLACK, \
    WHITE, SKY, FPS, FPS_FONT, FPS_SHOW_POS, SOUND_PLAY_MUSIC, \
    BIG_FONT, MASK_ALPHA, MUSIC_VOLUME
from level import Level
from support import draw_text
from overworld import Pause, MainMenu, DeathScene

class Game:
    def __init__(self, screen, clock) -> None:
        # Overworld creation
        self.screen = screen
        self.clock = clock
        self.main_menu = MainMenu(self.screen, ['Start', 'Exit'], self.create_level, self.exit_game, 0)
        self.status = 'main_menu'

        self.level = None
        self.pause = None

        self.paused = False
        self.death_scene = None

        # Sounds:
        self.level_bg_music = pygame.mixer.Sound('content/sounds/background.mp3')
        self.level_bg_music.set_volume(MUSIC_VOLUME)

    def create_level(self) -> None:
        self.screen.fill(BLACK)
        draw_text(self.screen, 'Loading...', BIG_FONT, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.level = Level(1, self.screen, self)
        self.status = 'level'
        if SOUND_PLAY_MUSIC: self.level_bg_music.play(loops=-1)

    def create_main_menu(self) -> None:
        self.main_menu = MainMenu(self.screen, ['Start', 'Exit'], self.create_level, self.exit_game, 0)
        self.status = 'main_menu'

    def create_pause(self) -> None:
        self.pause = Pause(self.screen, ['Return', 'Main Menu', 'Exit'], self.exit_game, self.stop_pause, self.create_main_menu, 0)
        self.status = 'pause'

    def stop_pause(self) -> None:
        self.status = 'level'

    def create_death_scene(self) -> None:
        self.death_scene = DeathScene(self.screen, ['Respawn', 'Main Menu', 'Exit'], self.create_main_menu, self.create_level, self.exit_game, 70)
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

    def show_fps(self) -> None:
        draw_text(self.screen, 'FPS: ' + str(int(self.clock.get_fps())), FPS_FONT, GREY, FPS_SHOW_POS[0], FPS_SHOW_POS[1])

    @staticmethod
    def exit_game() -> None:
        pygame.quit()
        sys.exit()

def print_mask(screen):
    mask = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    mask.fill(GREY)
    mask.set_alpha(MASK_ALPHA)
    screen.blit(mask, (SCREEN_WIDTH / 2 - mask.get_width() / 2, SCREEN_HEIGHT / 2 - mask.get_height() / 2))

def start_game():
    # Pygame setup
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()

    # Start game:
    game = Game(SCREEN, CLOCK)

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
            print_mask(game.screen)
            game.paused = True
        elif game.status == 'dead':
            SCREEN.fill(SKY)

        game.run_loop()

        game.show_fps()

        pygame.display.update()

        CLOCK.tick(FPS)