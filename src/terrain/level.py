"""
This module, level.py, defines the Level class responsible
for managing game levels, including terrain, players,
enemies, and various game elements.

The Level class manages the creation and behavior of game levels,
including loading level data, creating terrain and game elements,
handling player actions and movements, and managing enemy interactions.
It provides essential functions for running the game loop
and updating the game state during gameplay.
"""
import pygame
import tracemalloc
from terrain.images_manager import ImagesManager
from terrain.map_generator import generate_map, generate_enemies, create_tile_group
from tools.support import import_csv_file, now, draw_text, puts
from tools.game_data import levels
from tools.settings import TILE_SIZE, PLAYER_DEATH_LATENCY, ENEMY_DEATH_LATENCY, GREY, \
    SMALL_STATUS_FONT, PLAYER_SPAWN_POSITION
from terrain.tiles import check_for_usable_elements
from terrain.chest import Chest
from terrain.corpse import create_corpse
from terrain.collisions import vertical_movement_collision, horizontal_movement_collision, check_collisions
from terrain.items import Item
from terrain.items_generator import clean_items
from character.player import Player
from combat.fighting import FightManager
from terrain.camera import Camera
from terrain.animations import SoulAnimation


class Level:
    """
    Represents a game level and manages its components,
    including terrain, player, enemies, and more.
    """
    def __init__(self, level, surface, game):
        """
        Initialize the Level class.
        """
        # General setup
        self.display_surface = surface
        self.current_level = level
        self.pause = False
        self.game_over = False

        # Methods:
        self.create_pause = game.create_pause
        self.create_main_menu = game.create_main_menu
        self.create_death_scene = game.create_death_scene
        self.next_level = game.next_level

        # Check for game loading time
        loading_counter = pygame.time.get_ticks()

        # Fighting:
        self.fight_manager = FightManager()

        # Images:
        self.images = ImagesManager(self.display_surface)

        self.animations = []
        self.player = pygame.sprite.GroupSingle()
        self.terrain_sprite = pygame.sprite.Group()
        self.ter_near_sprites = pygame.sprite.Group()
        self.collideable_sprites = pygame.sprite.Group()
        self.col_near_sprites = pygame.sprite.Group()
        self.terrain_elements_sprite = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.camera = None

        self.configure_level()

        # Check for game loading time
        loading_time = str((pygame.time.get_ticks() - loading_counter) / 1000)
        print('Loading game time: ' + loading_time)

    def clear_groups(self, player: bool = False):
        clean_items(Item.items)
        if not player:
            puts('There has been a reset of the player')
            pygame.sprite.GroupSingle.empty(self.player)
        self.animations = []

        pygame.sprite.Group.empty(self.terrain_sprite)
        pygame.sprite.Group.empty(self.ter_near_sprites)
        pygame.sprite.Group.empty(self.collideable_sprites)
        pygame.sprite.Group.empty(self.col_near_sprites)
        pygame.sprite.Group.empty(self.terrain_elements_sprite)
        pygame.sprite.Group.empty(self.enemy_sprites)
        self.camera = None
        Chest.chests = []

        self.fight_manager.clear_groups()
        puts('Zresetowano level')

    def configure_level(self, player: bool = False):
        # Load level data:
        level_data = levels[1]
        self.game_over = False

        # Animations:
        self.animations = []

        # Player import:
        if not player:
            self.current_level = 1
            puts('Skonfigurowano gracza')
            player_layout = import_csv_file(level_data['player'])
            self.player_setup(player_layout)
        self.get_player().reset_position(PLAYER_SPAWN_POSITION)

        # Terrain import
        terrain_layout, terrain_elements_layout = generate_map()
        self.terrain_sprite = create_tile_group(terrain_layout, 'terrain', self.images, self, self.fight_manager)
        self.collideable_sprites = create_tile_group(terrain_layout, 'collideable', self.images, self, self.fight_manager)

        # Terrain elements import
        self.terrain_elements_sprite = create_tile_group(terrain_elements_layout, 'terrain_elements', self.images, self, self.fight_manager)

        # Enemy
        enemy_layout = generate_enemies(len(terrain_layout[0]) * TILE_SIZE)
        self.enemy_sprites = create_tile_group(enemy_layout, 'enemies', self.images, self, self.fight_manager)

        # Map camera configuration:
        self.camera = Camera(len(terrain_layout[0]) * TILE_SIZE, len(terrain_layout) * TILE_SIZE)

    def player_setup(self, layout):
        """
        Set up the player based on a layout.

        Args:
            layout (list): The layout specifying the player's position.
        """
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player(
                        (x, y),
                        self
                    )
                    self.player.add(sprite)

    def get_player(self):
        """
        Get the player sprite.

        Returns:
           Player: The player sprite.
        """
        for player in self.player:
            return player

    def find_near_tiles(self, player_pos):
        pygame.sprite.Group.empty(self.col_near_sprites)
        pygame.sprite.Group.empty(self.ter_near_sprites)

        for sprite in self.collideable_sprites:
            if self.camera.view[0] < sprite.rect.centerx - player_pos < self.camera.view[1]:
                self.col_near_sprites.add(sprite)
        for sprite in self.terrain_sprite:
            if self.camera.view[0] < sprite.rect.centerx - player_pos < self.camera.view[1]:
                self.ter_near_sprites.add(sprite)

    def run(self):
        """
        Run the game loop for the level.
        """
        drawing_all = now()
        self.display_surface.blit(self.images.background, (0, 0))

        player = self.get_player()
        player_pos = player.movement.collision_rect.centerx
        self.find_near_tiles(player_pos)

        # Fighting:
        self.fight_manager.attack_update(self.display_surface, self.camera.offset)
        self.fight_manager.check_damage(self.get_player(), self.enemy_sprites)

        # Draw terrain  -----------------------------------------------------------
        for sprite in self.col_near_sprites:
            sprite.update()
            sprite.draw(self.display_surface, self.camera.offset)
        for sprite in self.ter_near_sprites:
            sprite.update()
            sprite.draw(self.display_surface, self.camera.offset)
        for sprite in self.terrain_elements_sprite:
            if self.camera.view[0] < sprite.rect.centerx - player_pos < self.camera.view[1]:
                sprite.update()
                sprite.draw(self.display_surface, self.camera.offset)
        # Animations:
        for index, animation in enumerate(self.animations):
            animation.update(self.camera.offset)
            animation.draw(self.display_surface, self.camera.offset)
            if animation.finish:
                del animation
                self.animations.pop(index)

        # Draw player -----------------------------------------------------------
        if not self.game_over:
            self.player.update(self.display_surface)
            horizontal_movement_collision(player.movement, self.col_near_sprites)
            vertical_movement_collision(player.movement, self.col_near_sprites)
            self.camera.scroll_camera(self.display_surface.get_size(), player.movement)

            player.status.can_use_object = check_for_usable_elements(
                player,
                self.terrain_elements_sprite
            )
            if player.status.can_use_object[1] is not None and len(player.status.can_use_object[1]) > 0:
                player.status.can_use_object[1][0].pickable = True

            player.animations.draw(self.display_surface, self.camera.offset, player.status, player.movement)
            if player.properties.dead['status'] and \
                    pygame.time.get_ticks() - player.properties.dead['time'] > PLAYER_DEATH_LATENCY:
                self.create_death_scene()
                self.game_over = True
        # Draw enemies -----------------------------------------------------------
        enemy_counter = 0
        for enemy in self.enemy_sprites:
            if self.camera.view[0] < enemy.animations.rect.centerx - player_pos < self.camera.view[1]:
                enemy_counter += 1
                enemy.update()
                check_collisions(enemy.movement, self.col_near_sprites)
                if not enemy.properties.dead['status']:
                    enemy.animations.draw_health_bar(self.display_surface, self.camera.offset)
                    enemy.fighting.check_for_combat(self.get_player())
                enemy.animations.draw(self.display_surface, self.camera.offset)
                if enemy.properties.dead['status'] and \
                        now() - enemy.properties.dead['time'] > ENEMY_DEATH_LATENCY:
                    soul_animation = SoulAnimation(
                        enemy.animations.rect.center,
                        'soul',
                        self.display_surface.get_size()
                    )
                    self.animations.append(soul_animation)
                    create_corpse(self, enemy, self.terrain_elements_sprite)
                    enemy.kill()
        # Show UI -----------------------------------------------------------
        if not player.properties.dead['status']:
            player.ui.show_ui(self.display_surface, self.camera.offset, player)
        player.equipment.update_show(self.display_surface)

        # Developing
        memory_stats = tracemalloc.get_traced_memory()
        used_memory = round(memory_stats[0] / (1024 ** 2), 4)
        all_time = str((now() - drawing_all) / 1000)

        show_info(self.display_surface, f'Terrain elements: {self.terrain_elements_sprite}, lvl: {self.current_level}', 0)
        show_info(self.display_surface, f'Klocków: {len(self.col_near_sprites) + len(self.ter_near_sprites)}, enemies: {enemy_counter}/{len(self.enemy_sprites)}', 1)
        show_info(self.display_surface, f'Memory use [MB]: {used_memory}, loop time: {all_time} s.', 2)
        show_info(self.display_surface, f'Damage: {player.fighting.attack["damage"]}, skrzynie: {len(Chest.chests)}', 3)
        info = []
        for item in Item.items:
            info.append((item.name, item.owner[1]))
        #puts(info)


def show_info(screen, info, place) -> None:
    draw_text(screen, f'{info}', SMALL_STATUS_FONT, GREY, 750, 800+20*place, left=True)
