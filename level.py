import pygame
from support import import_csv_file, import_cut_graphics
from game_data import levels
from settings import TILE_SIZE, SCREEN_WIDTH
from tiles import StaticTile, AnimatedTile
from player import Player
from enemies import Sceleton, Ninja, Wizard, Dark_Knight
from fighting import Fight_Manager


class Level:
    def __init__(self, surface, create_pause, create_main_menu, create_death_scene):
        # General setup
        self.display_surface = surface
        self.offset = pygame.math.Vector2(0, 0)
        self.current_level = 1
        self.pause = False
        self.game_over = False

        # Load level data:
        level_data = levels[self.current_level]

        # Methods:
        self.create_pause = create_pause
        self.create_main_menu = create_main_menu
        self.create_death_scene = create_death_scene

        # Check for game loading time
        loading_counter = pygame.time.get_ticks()

        # Fighting:
        self.fight_manager = Fight_Manager()

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
        print('Czas ładowania gry: ' + loading_time)

        # Map borders configuration:
        self.border_left = 0
        self.border_right = len(terrain_layout[0]) * TILE_SIZE
        self.border_top = 0
        self.border_bottom = len(terrain_layout) * TILE_SIZE

    def create_tile_group(self, layout, kind):
        sprite_group = pygame.sprite.Group()
        terrain_tile_list: list = []
        enemy_id: int = 0
        tile_id: int = 0
        sprite: object = None

        # Load tile sets:
        if kind == 'terrain':
            terrain_tile_list = import_cut_graphics('content/graphics/terrain/terrain_tiles.png', (TILE_SIZE, TILE_SIZE))

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != str(-1):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if kind == 'terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_id, TILE_SIZE, x, y, tile_surface)
                        tile_id += 1

                    if kind == 'terrain_elements':
                        if val == '0':
                            sprite = AnimatedTile(tile_id, TILE_SIZE, x, y, 'content/graphics/terrain/fireplace/')
                            tile_id += 1

                    if kind == 'enemies':
                        if val == '0':
                            sprite = Sceleton(enemy_id, (x, y), self.fight_manager.sword_attack)
                            enemy_id += 1
                        if val == '1':
                            sprite = Ninja(enemy_id, (x, y), self.fight_manager.arch_attack)
                            enemy_id += 1
                        if val == '2':
                            sprite = Wizard(enemy_id, (x, y), self.fight_manager.arch_attack, self.fight_manager.thunder_attack)
                            enemy_id += 1
                        if val == '3':
                            sprite = Dark_Knight(enemy_id, (x, y), self.fight_manager.sword_attack)
                            enemy_id += 1
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y), self.create_pause,
                                    self.fight_manager.sword_attack, self.fight_manager.arch_attack)
                    self.player.add(sprite)

    def get_player(self):
        for player in self.player:
            return player

    def scroll_camera(self):
        half_w = self.display_surface.get_size()[0] / 2
        half_h = self.display_surface.get_size()[1] / 2
        player = self.player.sprite

        offset_x = self.offset.x
        offset_y = self.offset.y

        # Check X offset
        if self.border_right - half_w > player.collision_rect.centerx > half_w:
            offset_x = player.collision_rect.centerx - half_w
        if player.collision_rect.centerx < half_w:
            offset_x = 0
        if player.collision_rect.centerx > self.border_right - half_w:
            offset_x = self.border_right - 2 * half_w
        # Check Y offset
        if self.border_bottom - half_h > player.collision_rect.centery > half_h:
            offset_y = player.collision_rect.centery - half_h
        if player.collision_rect.centery < half_h:
            offset_y = 0
        if player.collision_rect.centery > self.border_bottom - half_h:
            offset_y = self.border_bottom - 2 * half_h

        self.offset.x = offset_x
        self.offset.y = offset_y

    def horizontal_movement_collision(self, character):

        character.collision_rect.x += character.direction.x * character.speed
        collidable_sprites = self.terrain_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(character.collision_rect):
                if sprite.rect.centerx < character.collision_rect.centerx:
                    character.collision_rect.left = sprite.rect.right
                    character.on_right = False
                    character.on_left = True

                elif sprite.rect.centerx > character.collision_rect.centerx:
                    character.collision_rect.right = sprite.rect.left
                    character.on_right = True
                    character.on_left = False

    def vertical_movement_collision(self, character):

        character.apply_gravity()
        collidable_sprites = self.terrain_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(character.collision_rect):
                if character.direction.y > 0 and sprite.rect.centery > character.collision_rect.centery:  # Falling
                    character.collision_rect.bottom = sprite.rect.top
                    character.direction.y = 0
                    character.on_ground = True
                elif character.direction.y < 0 and sprite.rect.centery < character.collision_rect.centery:
                    character.collision_rect.top = sprite.rect.bottom
                    character.direction.y = 0
        if character.on_ground and character.direction.y < 0 or character.direction.y > 1:
            character.on_ground = False

    def run(self):

        # Fighting:
        self.fight_manager.attack_update(self.display_surface, self.offset)
        self.fight_manager.check_damage(self.get_player(), self.enemy_sprites)

        player_pos = self.get_player().collision_rect.centerx
        # Run the entire game / level
        for sprite in self.terrain_sprite:
            if abs(sprite.rect.centerx - player_pos) < SCREEN_WIDTH:
                sprite.update()
                sprite.draw(self.display_surface, self.offset)
        for sprite in self.terrain_elements_sprite:
            if abs(sprite.rect.centerx - player_pos) < SCREEN_WIDTH:
                sprite.update()
                sprite.draw(self.display_surface, self.offset)

        # Draw player
        player = self.get_player()
        if not self.game_over:
            self.player.update(self.display_surface, self.offset)
            self.horizontal_movement_collision(self.player.sprite)
            self.vertical_movement_collision(self.player.sprite)
            self.scroll_camera()

            player.draw(self.display_surface, self.offset)
            if player.dead and pygame.time.get_ticks() - player.dead_time > 2000:
                self.create_death_scene()
                self.game_over = True

        # Enemy
        self.enemy_sprites.update(self.offset)
        for enemy in self.enemy_sprites:
            if abs(enemy.rect.centerx - player_pos) < SCREEN_WIDTH:
                self.horizontal_movement_collision(enemy)
                self.vertical_movement_collision(enemy)
                if not enemy.dead:
                    enemy.draw_health_bar(self.display_surface, self.offset)
                    enemy.check_for_combat(self.get_player())
                enemy.draw(self.display_surface, self.offset)
            if enemy.dead and pygame.time.get_ticks() - enemy.dead_time > 3000:
                enemy.kill()

        # Show UI:
        if player.dead == False:
            player.ui.show_ui(self.display_surface, self.offset, (player.max_health, player.health), (
            player.sword_can_attack, player.sword_attack_time, player.sword_attack_cooldown, player.collision_rect), \
                              player.equipment.active_items, player.equipment)



