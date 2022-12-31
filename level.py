import pygame
from support import import_csv_file, import_cut_graphics, draw_text
from game_data import levels
from settings import TILE_SIZE, SCREEN_WIDTH, BLACK, ATTACK_SPACE
from tiles import StaticTile
from player import Player
from enemies import Sceleton, Ninja
from attack import Hit, Bullet


class Level:
    def __init__(self, surface, create_pause, create_main_menu, create_death_scene, font):
        # General setup
        self.normal_font = font
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
        self.border_top = 0
        self.border_bottom = len(terrain_layout) * TILE_SIZE

        # Sword sword_attacking:
        self.sword_hits = pygame.sprite.Group()
        self.bullet_hits = pygame.sprite.Group()

    def create_tile_group(self, layout, kind):
        sprite_group = pygame.sprite.Group()
        counter = pygame.time.get_ticks()
        enemy_id = 0
        tile_id = 0
        sprite = 0
        # Load tile sets:
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

        time = str((pygame.time.get_ticks() - counter) / 1000)
        print('Czas ładowania gry: ' + time)
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y), self.normal_font, self.create_pause,
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

    def vertical_movement_collision(self, thing):
        person = thing
        person.apply_gravity()
        collidable_sprites = self.terrain_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(person.collision_rect):
                if person.direction.y > 0 and sprite.rect.centery > person.collision_rect.centery:  # Falling
                    person.collision_rect.bottom = sprite.rect.top
                    person.direction.y = 0
                    person.on_ground = True
                elif person.direction.y < 0 and sprite.rect.centery < person.collision_rect.centery:
                    person.collision_rect.top = sprite.rect.bottom
                    person.direction.y = 0
        if person.on_ground and person.direction.y < 0 or person.direction.y > 1:
            person.on_ground = False

    def sword_attack(self, source, source_id, collision_rect, facing_right, damage, can_attack, width):
        if can_attack:

            if source == 'player':
                space = ATTACK_SPACE
            else:
                space = 5

            if facing_right:
                pos = (collision_rect.centerx + space, collision_rect.top)
            else:
                pos = (collision_rect.centerx - width - space, collision_rect.top)

            hit = Hit(pos, damage, source, source_id, width)
            self.sword_hits.add(hit)

    def arch_attack(self, source, collision_rect, facing_right, damage, can_attack):
        if can_attack:

            if facing_right:
                pos = (collision_rect.right, collision_rect.top + collision_rect.height / 3)
            else:
                pos = (collision_rect.left + 20, collision_rect.top + collision_rect.height / 3)

            bullet = Bullet(pos, damage, source, facing_right)
            self.bullet_hits.add(bullet)

    def check_damage(self):
        # Sword hits:
        sword_collisions_enemy = []
        sword_collisions_player = []
        arrow_collisions_enemy = []
        arrow_collisions_player = []
        source = 'default'
        dmg = 0

        def player_got_hurt():
            character = self.get_player()
            character.just_hurt = True
            character.just_hurt_time = pygame.time.get_ticks()
            character.health -= dmg
            if character.health <= 0:  # Death of player
                character.dead = True
                character.status = 'dead'
                character.frame_index = 0
                character.direction.x = 0
                character.dead_time = pygame.time.get_ticks()

        for hit in self.sword_hits:  # Check any melee hits collisions
            for enemy in self.enemy_sprites:
                if hit.rect.colliderect(enemy.collision_rect):
                    sword_collisions_enemy.append(enemy)
            for player in self.player:
                if hit.rect.colliderect(player.collision_rect) and not hit.shielded:
                    if player.shielding:

                        for enemy in self.enemy_sprites:
                            if enemy.id == hit.source_id:
                                if ((player.facing_right and enemy.collision_rect.x > player.collision_rect.x) or
                                    (not player.facing_right and enemy.collision_rect.x < player.collision_rect.x)):
                                    self.shield_block_sound.play()
                                    hit.shielded = True
                                    if not enemy.stunned:
                                        enemy.stunned = True
                                        enemy.status = 'stun'
                                        enemy.armor_ratio = 3
                                        break
                                else:
                                    sword_collisions_player.append(player)

                    else:
                        sword_collisions_player.append(player)

            dmg = hit.damage
            source = hit.source
        if sword_collisions_enemy:  # If there is melee attack collision with enemies:
            for enemy in sword_collisions_enemy:
                if not enemy.just_hurt and source == 'player':
                    enemy.just_hurt = True
                    enemy.just_hurt_time = pygame.time.get_ticks()
                    enemy.health -= dmg * enemy.armor_ratio
                    if enemy.health <= 0:  # Death of enemy
                        enemy.dead = True
                        enemy.status = 'dead'
                        enemy.frame_index = 0
                        enemy.dead_time = pygame.time.get_ticks()

                        self.get_player().ui.add_experience(self.get_player().experience, enemy.experience)
                        self.get_player().experience += enemy.experience
        if sword_collisions_player:  # If there is melee attack collision with player:
            player = self.get_player()
            if not player.just_hurt and source == 'enemy':
                player_got_hurt()

        for bullet in self.bullet_hits:  # Check any bullet hits collisions
            point = False
            if bullet.source == 'player':
                for enemy in self.enemy_sprites:
                    if bullet.rect.colliderect(enemy.collision_rect):
                        arrow_collisions_enemy.append(enemy)
                        point = True
            if bullet.source == 'enemy':
                for player in self.player:
                    if bullet.rect.colliderect(player.collision_rect) and not bullet.shielded:
                        if player.shielding:
                            self.shield_block_sound.play()
                            bullet.shielded = True
                        else:
                            arrow_collisions_player.append(player)
                        point = True
            dmg = bullet.damage
            source = bullet.source
            if point:
                bullet.kill()

        if arrow_collisions_enemy:  # If there is bullet collision with enemies:
            for enemy in arrow_collisions_enemy:
                if not enemy.just_hurt and source == 'player':
                    enemy.just_hurt = True
                    enemy.just_hurt_time = pygame.time.get_ticks()
                    enemy.health -= dmg
                    if enemy.health <= 0:  # Death of enemy
                        enemy.dead = True
                        enemy.status = 'dead'
                        enemy.dead_time = pygame.time.get_ticks()

                        self.get_player().ui.add_experience(self.get_player().experience, enemy.experience)
                        self.get_player().experience += enemy.experience
        if arrow_collisions_player:  # If there is bullet collision with player:
            player = self.get_player()
            if not player.just_hurt and not player.shielding and source == 'enemy':
                player_got_hurt()

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
            for player in self.player:
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
        self.sword_hits.update("HALO")
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

        # Show information for developer
        draw_text(self.display_surface, 'Player pos: ' + str(self.get_player().rect.center),
                  self.normal_font, BLACK, SCREEN_WIDTH / 2, 50)
        # draw_text(self.display_surface, 'Status: ' + str(self.get_player().status),
        # self.normal_font, BLACK,SCREEN_WIDTH / 2, 70)
        draw_text(self.display_surface, 'Frame index: ' + str(int(self.get_player().frame_index)),
                  self.normal_font, BLACK, SCREEN_WIDTH / 2, 80)
