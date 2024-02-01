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
from tools.support import import_csv_file, import_cut_graphics, scale_image, import_image, now
from tools.game_data import levels
from tools.settings import PRIMAL_TILE_SIZE, TILE_SIZE, SCREEN_WIDTH, \
    TERRAIN_PATH, FIREPLACE_PATH, CHEST_PATH, PLAYER_DEATH_LATENCY, ENEMY_DEATH_LATENCY
from tiles import StaticTile, Bonfire, Chest, check_for_usable_elements, create_corpse
from terrain.collisions import vertical_movement_collision, horizontal_movement_collision
from player.player import Player
from entities.enemies import Sceleton, Ninja, Wizard, DarkKnight
from entities.fighting import Fight_Manager
from terrain.camera import Camera
from animations import SoulAnimation


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

        # Load level data:
        level_data = levels[self.current_level]

        # Methods:
        self.create_pause = game.create_pause
        self.create_main_menu = game.create_main_menu
        self.create_death_scene = game.create_death_scene

        # Check for game loading time
        loading_counter = pygame.time.get_ticks()

        # Fighting:
        self.fight_manager = Fight_Manager()

        # Background:
        self.background = import_image('content/graphics/terrain/background.png')
        self.background = scale_image(self.background, self.display_surface.get_size())

        # Animations:
        self.animations = []

        # Player import:
        player_layout = import_csv_file(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain import
        terrain_layout = import_csv_file(level_data['terrain'])
        self.terrain_sprite = self.create_tile_group(terrain_layout, 'terrain')

        # Terrain elements import
        terrain_elements_layout = import_csv_file(level_data['terrain_elements'])
        self.terrain_elements_sprite = self.create_tile_group(terrain_elements_layout, 'terrain_elements')

        # Enemy
        enemy_layout = import_csv_file(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Check for game loading time
        loading_time = str((pygame.time.get_ticks() - loading_counter) / 1000)
        print('Loading game time: ' + loading_time)

        # Map camera configuration:
        self.camera = Camera(len(terrain_layout[0]) * TILE_SIZE,len(terrain_layout) * TILE_SIZE)

    def create_tile_group(self, layout, kind):
        """
        Create a group of tiles from a layout.

        Args:
            layout (list): The layout specifying the arrangement of tiles.
            kind (str): The kind of tiles to create.

        Returns:
            pygame.sprite.Group: A group of sprite objects representing the tiles.
        """
        sprite_group = pygame.sprite.Group()
        terrain_tile_list: list = []
        enemy_id: int = 0
        tile_id: int = 0
        sprite: object = None

        # Load tile sets:
        if kind == 'terrain':
            terrain_tile_list = import_cut_graphics(TERRAIN_PATH, (PRIMAL_TILE_SIZE, PRIMAL_TILE_SIZE))

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != str(-1):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if kind == 'terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        tile_surface = scale_image(tile_surface, (TILE_SIZE, TILE_SIZE))
                        sprite = StaticTile(tile_id, TILE_SIZE, x, y, tile_surface)
                        tile_id += 1

                    if kind == 'terrain_elements':
                        if val == '1':
                            sprite = Bonfire(tile_id, TILE_SIZE, x, y, FIREPLACE_PATH)
                            tile_id += 1
                        if val == '0':
                            sprite = Chest(tile_id, TILE_SIZE, x, y, CHEST_PATH)
                            tile_id += 1

                    if kind == 'enemies':
                        if val == '0':
                            sprite = Sceleton(
                                enemy_id,
                                (x, y),
                                self.fight_manager.sword_attack
                            )
                            enemy_id += 1
                        if val == '1':
                            sprite = Ninja(
                                enemy_id,
                                (x, y),
                                self.fight_manager.arch_attack
                            )
                            enemy_id += 1
                        if val == '2':
                            sprite = Wizard(
                                enemy_id,
                                (x, y),
                                self.fight_manager.arch_attack,
                                self.fight_manager.thunder_attack
                            )
                            enemy_id += 1
                        if val == '3':
                            sprite = DarkKnight(
                                enemy_id,
                                (x, y),
                                self.fight_manager.sword_attack
                            )
                            enemy_id += 1
                    sprite_group.add(sprite)
        return sprite_group

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
                        self.create_pause,
                        self.fight_manager.sword_attack,
                        self.fight_manager.arch_attack
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

    def run(self):
        """
        Run the game loop for the level.
        """
        self.display_surface.blit(self.background, (0, 0))

        player = self.get_player()
        player_pos = player.movement.collision_rect.centerx
        # Fighting:
        self.fight_manager.attack_update(self.display_surface, self.camera.offset)
        self.fight_manager.check_damage(self.get_player(), self.enemy_sprites)
        # Draw terrain  -----------------------------------------------------------
        for sprite in self.terrain_sprite:
            if abs(sprite.rect.centerx - player_pos) < SCREEN_WIDTH:
                sprite.update()
                sprite.draw(self.display_surface, self.camera.offset)
        for sprite in self.terrain_elements_sprite:
            if abs(sprite.rect.centerx - player_pos) < SCREEN_WIDTH:
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
            horizontal_movement_collision(player.movement, self.terrain_sprite)
            vertical_movement_collision(player.movement, self.terrain_sprite)
            self.camera.scroll_camera(self.display_surface.get_size(), player.movement)

            player.status.can_use_object = check_for_usable_elements(
                player,
                self.terrain_elements_sprite
            )

            player.animations.draw(self.display_surface, self.camera.offset)
            if player.properties.dead['status'] and \
                    pygame.time.get_ticks() - player.properties.dead['time'] > PLAYER_DEATH_LATENCY:
                self.create_death_scene()
                self.game_over = True
        # Draw enemies -----------------------------------------------------------
        for enemy in self.enemy_sprites:
            enemy.update()
            if abs(enemy.animations.rect.centerx - player_pos) < SCREEN_WIDTH:
                horizontal_movement_collision(enemy.movement, self.terrain_sprite)
                vertical_movement_collision(enemy.movement, self.terrain_sprite)
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
                create_corpse(enemy, self.terrain_elements_sprite)
                enemy.kill()
        # Show UI -----------------------------------------------------------
        if not player.properties.dead['status']:
            player.ui.show_ui(self.display_surface, self.camera.offset, player)
        player.equipment.update_show(self.display_surface)
