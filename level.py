import pygame
from support import import_csv_file, import_cut_graphics
from game_data import levels
from settings import TILE_SIZE, ATTACK_SPACE, ENEMY_SPACE
from tiles import StaticTile
from player import Player
from enemies import Sceleton, Ninja
from fighting import Hit, Bullet


class Level:
    def __init__(self, surface, create_pause, create_main_menu, create_death_scene):
        # General setup
        self.display_surface = surface
        self.offset = pygame.math.Vector2(0, 0)
        self.current_level = 0
        self.pause = False
        self.game_over = False

        # Sounds:
        self.shield_block_sound = pygame.mixer.Sound('content/sounds/character/shield_block.mp3')

        # Load level data:
        level_data = levels[self.current_level]

        # Methods:
        self.create_pause = create_pause
        self.create_main_menu = create_main_menu
        self.create_death_scene = create_death_scene

        # Check for game loading time
        loading_counter = pygame.time.get_ticks()

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

        # Check for game loading time
        loading_time = str((pygame.time.get_ticks() - loading_counter) / 1000)
        print('Czas ładowania gry: ' + loading_time)

        # Map borders configuration:
        self.border_left = 0
        self.border_right = len(terrain_layout[0]) * TILE_SIZE
        self.border_top = 0
        self.border_bottom = len(terrain_layout) * TILE_SIZE

        # Fighting:
        self.sword_hits = pygame.sprite.Group()
        self.bullet_hits = pygame.sprite.Group()

    def create_tile_group(self, layout, kind):
        sprite_group = pygame.sprite.Group()
        terrain_tile_list: list = []
        enemy_id: int = 0
        tile_id: int = 0
        sprite: object = None

        # Load tile sets:
        if kind == 'terrain':
            terrain_tile_list = import_cut_graphics('content/graphics/terrain/terrain_tiles.png')

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != str(-1):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if kind == 'terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_id, TILE_SIZE, x, y, tile_surface)
                        tile_id += 1

                    if kind == 'enemies':
                        if val == '0':
                            sprite = Sceleton(enemy_id, (x, y), self.sword_attack)
                            enemy_id += 1
                        if val == '1':
                            sprite = Ninja(enemy_id, (x, y), self.arch_attack)
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
                                    self.sword_attack, self.arch_attack)
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

    def sword_attack(self, source, source_id, collision_rect, facing_right, damage, can_attack, width):
        if can_attack:

            if source == 'player':
                space = ATTACK_SPACE
            else:
                space = ENEMY_SPACE

            if facing_right:
                position = (collision_rect.centerx + space, collision_rect.top)
            else:
                position = (collision_rect.centerx - width - space, collision_rect.top)

            hit = Hit(position, damage, source, source_id, width)
            self.sword_hits.add(hit)

    def arch_attack(self, source, source_id, collision_rect, facing_right, damage, can_attack):
        if can_attack:

            if facing_right:
                position = (collision_rect.right, collision_rect.top + collision_rect.height / 3)
            else:
                position = (collision_rect.left + 20, collision_rect.top + collision_rect.height / 3)

            bullet = Bullet(position, damage, source, source_id, facing_right)
            self.bullet_hits.add(bullet)

    def check_damage(self):
        # Hit groups:
        sword_collisions = []
        arrow_collisions = []
        source = 'default'
        damage = 0

        def character_kill(character) -> None:
            character.dead = True
            character.status = 'dead'
            character.frame_index = 0
            character.direction.x = 0
            character.dead_time = pygame.time.get_ticks()

            if character.type != 'Player':
                self.get_player().add_experience(character.experience)

        def character_hurt(character, damage) -> None:
            character.just_hurt = True
            character.just_hurt_time = pygame.time.get_ticks()
            character.health -= damage * character.armor_ratio
            if character.health <= 0:  # Death of player
                character_kill(character)

        def character_search_hit_collisions(kind, hits, player, enemies, collisions_group) -> None:
            for hit in hits:  # Check for any hits collisions
                point = False # if kind of hits is 'bullets'
                for enemy in enemies:
                    if hit.rect.colliderect(enemy.collision_rect) and hit.source == 'player': # If enemy get hit by player
                        collisions_group.append((enemy, hit.damage, hit.source))
                        if kind == 'bullet': point = True

                if hit.rect.colliderect(player.collision_rect) and not hit.shielded and hit.source != 'player': # If player get hit by enemy
                    if player.shielding:
                        for enemy in enemies:
                            if enemy.id == hit.source_id:
                                if ((player.facing_right and enemy.collision_rect.x > player.collision_rect.x) or
                                    (not player.facing_right and enemy.collision_rect.x < player.collision_rect.x)):
                                    self.shield_block_sound.play()
                                    hit.shielded = True
                                    if not enemy.stunned and kind == 'sword':
                                        enemy.stunned = True
                                        enemy.status = 'stun'
                                        enemy.armor_ratio = 3
                                        break
                                else:
                                    collisions_group.append((player, hit.damage, hit.source))
                    else:
                        collisions_group.append((player, hit.damage, hit.source))

                    if kind == 'bullet': point = True

                if point and kind == 'bullet': # Destroy bullet after collision with anyone
                    hit.kill()
        def character_hit_collisions(collisions) -> None:
            if collisions:  # If there is melee attack collision with enemies:
                for collision in collisions:
                    character = collision[0]
                    damage = collision[1]
                    source = collision[2].lower()

                    if not character.just_hurt and character.type.lower() != 'player' and source == 'player':
                        character_hurt(character, damage)
                    if not character.just_hurt and character.type.lower() == 'player' and source != 'player':
                        character_hurt(character, damage)

        character_search_hit_collisions('sword', self.sword_hits, self.get_player(), self.enemy_sprites, sword_collisions)
        character_hit_collisions(sword_collisions)

        character_search_hit_collisions('bullet', self.bullet_hits, self.get_player(), self.enemy_sprites, arrow_collisions)
        character_hit_collisions(arrow_collisions)

    def run(self):
        # Run the entire game / level
        self.terrain_sprite.update(self.offset)
        for sprite in self.terrain_sprite:
            sprite.draw(self.display_surface, self.offset)

        # Draw player
        if not self.game_over:
            self.player.update(self.display_surface, self.offset)
            self.horizontal_movement_collision(self.player.sprite)
            self.vertical_movement_collision(self.player.sprite)
            self.scroll_camera()

            player = self.get_player()
            player.draw(self.display_surface, self.offset)
            if player.dead and pygame.time.get_ticks() - player.dead_time > 2000:
                self.create_death_scene()
                self.game_over = True

        # Enemy
        self.enemy_sprites.update(self.offset)
        for enemy in self.enemy_sprites:
            self.horizontal_movement_collision(enemy)
            self.vertical_movement_collision(enemy)
            if not enemy.dead:
                enemy.draw_health_bar(self.display_surface, self.offset)
                enemy.check_for_combat(self.get_player())
            enemy.draw(self.display_surface, self.offset)
            if enemy.dead and pygame.time.get_ticks() - enemy.dead_time > 3000:
                enemy.kill()

        # Attacks:
        self.sword_hits.update()
        for hit in self.sword_hits:
            hit.draw(self.display_surface, self.offset)
            if pygame.time.get_ticks() - hit.attack_time > hit.attack_duration:
                hit.kill()

        self.bullet_hits.update()
        for bullet in self.bullet_hits:
            bullet.draw(self.display_surface, self.offset)
            if pygame.time.get_ticks() - bullet.attack_time > bullet.attack_duration:
                bullet.kill()

        # Damages:
        self.check_damage()

        # Show UI:
        self.get_player().show_ui(self.display_surface, self.offset)


