import pygame
from support import import_csv_file, import_cut_graphics
from game_data import levels
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, ATTACK_SIZE, ATTACK_SPACE
from tiles import StaticTile
from player import Player
from enemies import Sceleton
from buttons import Return_Button, Exit_Button
from attack import Hit


class Level:
    def __init__(self, surface, create_pause):
        # General setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_level = 0
        self.pause = False

        # Load level data:
        level_data = levels[self.current_level]

        # Methods:
        self.create_pause = create_pause

        # Player import:
        player_layout = import_csv_file(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain import
        terrain_layout = import_csv_file(level_data['terrain'])
        self.terrain_sprite = self.create_tile_group(terrain_layout, 'terrain')

        # Enemy
        enemy_layout = import_csv_file(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Map borders configuration:
        self.border_left = 0
        self.border_right = len(terrain_layout[0]) * TILE_SIZE

        # Sword sword_attacking:
        self.sword_hits = pygame.sprite.Group()


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        stoper = pygame.time.get_ticks()
        enemy_id = 1
        # Load tilesets:
        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != str(-1):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    if type == 'enemies':
                        sprite = Sceleton((x, y), self.sword_attack, enemy_id)
                        enemy_id += 1
                    sprite_group.add(sprite)

        time = str((pygame.time.get_ticks() - stoper)  / 1000)
        print('Czas: ' + time)
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_pause, self.sword_attack)
                    self.player.add(sprite)

    def get_player(self):
        for player in self.player:
            return player

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 3 and direction_x < 0 and self.border_left < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH * 2 / 3 and direction_x > 0 and self.border_right > SCREEN_WIDTH:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

        self.border_left += self.world_shift
        self.border_right += self.world_shift

    def horizontal_movement_collision(self, thing):
        person = thing
        person.collision_rect.x += person.direction.x * person.speed
        collidable_sprites = self.terrain_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(person.collision_rect):
                if sprite.rect.centerx < person.collision_rect.centerx:
                    person.collision_rect.left = sprite.rect.right
                    person.on_right = False
                    person.on_left = True

                elif sprite.rect.centerx > person.collision_rect.centerx:
                    person.collision_rect.right = sprite.rect.left
                    person.on_right = True
                    person.on_left = False
            # else:
            #     person.on_right = False
            #     person.on_left = False


    def vertical_movement_collision(self, thing):
        person = thing
        person.apply_gravity()
        collidable_sprites = self.terrain_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(person.collision_rect):
                if person.direction.y > 0 and sprite.rect.centery > person.collision_rect.centery: # Falling
                    person.collision_rect.bottom = sprite.rect.top
                    person.direction.y = 0
                    person.on_ground = True
                elif person.direction.y < 0 and sprite.rect.centery < person.collision_rect.centery:
                    person.collision_rect.top = sprite.rect.bottom
                    person.direction.y = 0
        if person.on_ground and person.direction.y < 0 or person.direction.y > 1:
            person.on_ground = False

    def sword_attack(self, who, rect, facing, damage, can_attack):
        source = who
        collision_rect = rect
        facing_right = facing

        if source == 'player': space = ATTACK_SPACE
        else: space = 15

        if facing_right == True:
            pos = (collision_rect.left + space, collision_rect.top)
        else:
            pos = (collision_rect.right - ATTACK_SIZE[0] - space, collision_rect.top)
        if can_attack:
            hit = Hit(pos, damage, source)
            self.sword_hits.add(hit)

    def check_sword_attack_duration(self):
        for hit in self.sword_hits:
            if pygame.time.get_ticks() - hit.attack_time > hit.attack_duration:
                hit.kill()

    def check_damage(self):
        # Sword hits:
        sword_collisions_enemy = []
        sword_collisions_player = []
        dmg = 0
        for hit in self.sword_hits:
            sword_collisions_enemy = pygame.sprite.spritecollide(hit, self.enemy_sprites, False)
            sword_collisions_player = pygame.sprite.spritecollide(hit, self.player, False)
            dmg = hit.damage
            source = hit.source
        if sword_collisions_enemy:
            for enemy in sword_collisions_enemy:
                if not enemy.just_hitted and source == 'player':
                    enemy.just_hitted = True
                    enemy.just_hitted_time = pygame.time.get_ticks()
                    enemy.health -= dmg
                    if enemy.health <= 0:
                        enemy.kill()
                        self.get_player().experience += enemy.experience
        if sword_collisions_player:
            player = self.get_player()
            if not player.just_hitted and source == 'enemy':
                player.just_hitted = True
                player.just_hitted_time = pygame.time.get_ticks()
                player.health -= dmg
                if player.health <= 0: enemy.kill()



    def run(self):


        # Run the entire game / level
        self.terrain_sprite.update(self.world_shift)
        self.terrain_sprite.draw(self.display_surface)

        # Draw player
        self.player.update(self.display_surface)
        self.horizontal_movement_collision(self.player.sprite)
        self.vertical_movement_collision(self.player.sprite)
        self.scroll_x()
        self.player.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        for enemy in self.enemy_sprites:
            self.horizontal_movement_collision(enemy)
            self.vertical_movement_collision(enemy)
            enemy.draw_health_bar(self.display_surface)
            enemy.check_for_combat(self.get_player())
        self.enemy_sprites.draw(self.display_surface)

        # Attacks:
        self.sword_hits.update(self.world_shift)
        self.sword_hits.draw(self.display_surface)
        self.check_sword_attack_duration()

        # Damages:
        self.check_damage()
