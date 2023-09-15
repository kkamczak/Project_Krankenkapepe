import pygame
from settings import YELLOW, RED, PLAYER_ATTACK_SIZE, SHOW_HIT_RECTANGLES, BULLET_DEFAULT_SPEED, \
    SCREEN_HEIGHT, ENEMY_ATTACK_SIZE

class Hit(pygame.sprite.Sprite):
    def __init__(self, pos, damage, source, source_id):
        super().__init__()
        # Create surface
        self.source = source
        self.source_id = source_id
        if self.source == 'player':
            size = PLAYER_ATTACK_SIZE
        else:
            size = ENEMY_ATTACK_SIZE[self.source]

        self.image = pygame.Surface(size)
        self.image.fill(RED)
        if SHOW_HIT_RECTANGLES: self.image.set_alpha(50)
        else: self.image.set_alpha(0)

        self.rect = self.image.get_rect(topleft = pos)

        self.attack_time = pygame.time.get_ticks()
        self.attack_duration = 100

        self.damage = damage
        self.shielded = False
        self.character_collided = []

    def update(self):
        pass
    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, kind, pos, damage, source, source_id, facing_right):
        super().__init__()

        self.kind = kind
        self.source = source
        self.source_id = source_id

        self.image = pygame.image.load(f'content/graphics/weapons/{self.kind}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect((pos), (5, 5))

        self.facing_right = facing_right

        if not self.facing_right:
            self.direction = pygame.math.Vector2(-1, 0)
        else:
            self.direction = pygame.math.Vector2(1, 0)
            flipped_image = pygame.transform.flip(self.image, True, False)
            self.image = flipped_image

        self.speed = BULLET_DEFAULT_SPEED[self.kind]

        self.attack_time = pygame.time.get_ticks()
        self.attack_duration = 1500

        self.damage = damage
        self.shielded = False
        self.character_collided = []

    def update(self):
        self.collision_rect.x += self.direction.x * self.speed
        if self.facing_right:
            self.rect.topright = self.collision_rect.topright
            self.rect = self.image.get_rect(topright=self.rect.topright)
        else:
            self.rect.topleft = self.collision_rect.topleft
            self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class Thunder(pygame.sprite.Sprite):
    def __init__(self, pos, damage, source, source_id):
        super().__init__()
        self.source = source
        self.source_id = source_id

        self.width = 60
        self.height = 1500
        self.position = [pos.centerx - self.width/2, pos.bottom-SCREEN_HEIGHT]

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        self.image.set_alpha(30)

        #self.rect = self.image.get_rect(midbottom=pos)
        self.collision_rect = pygame.Rect(self.position, (self.width, self.height))
        self.rect = self.collision_rect

        self.speed = 1.5

        self.attack = False
        self.attack_time = pygame.time.get_ticks()
        self.attack_duration = 600

        self.damage = damage
        self.shielded = False
        self.character_collided = []

    def update(self):
        if self.width > 10:
            self.width -= self.speed
            self.position[0] += (self.speed / 2)
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(YELLOW)
            self.image.set_alpha(30)
            self.collision_rect = pygame.Rect((self.position), (self.width, self.height))
            self.rect = self.collision_rect
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)
            self.image.set_alpha(80)
            self.collision_rect = pygame.Rect(self.position, (self.width, self.height))
            self.rect = self.collision_rect
            if not self.attack:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()

    def draw(self, surface, offset):
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)

class Fight_Manager():
    def __init__(self):
        # Fighting:
        self.sword_hits = pygame.sprite.Group()
        self.bullet_hits = pygame.sprite.Group()
        self.thunder_hits = pygame.sprite.Group()

        # Sounds:
        self.shield_block_sound = pygame.mixer.Sound('content/sounds/character/shield_block.mp3')
        self.shield_block_sound.set_volume(0.05)
    def sword_attack(self, source, source_id, collision_rect, facing_right, damage, can_attack, width, space, hit_height):
        if can_attack:
            if facing_right:
                position = (collision_rect.centerx + space, collision_rect.bottom - hit_height)
            else:
                position = (collision_rect.centerx - width - space, collision_rect.bottom - hit_height)

            hit = Hit(position, damage, source, source_id)
            self.sword_hits.add(hit)

    def arch_attack(self, kind, source, source_id, collision_rect, facing_right, damage, can_attack):
        if can_attack:

            if facing_right:
                position = (collision_rect.right, collision_rect.top + collision_rect.height / 3)
            else:
                position = (collision_rect.left + 20, collision_rect.top + collision_rect.height / 3)

            bullet = Bullet(kind, position, damage, source, source_id, facing_right)
            self.bullet_hits.add(bullet)

    def thunder_attack(self, source, source_id, position, damage, can_attack):
        if can_attack:
            thunder = Thunder(position, damage, source, source_id)
            self.thunder_hits.add(thunder)

    def attack_update(self, surface, offset):
        # Attacks:
        self.sword_hits.update()
        for hit in self.sword_hits:
            hit.draw(surface, offset)
            if pygame.time.get_ticks() - hit.attack_time > hit.attack_duration:
                hit.kill()

        self.bullet_hits.update()
        for bullet in self.bullet_hits:
            bullet.draw(surface, offset)
            if pygame.time.get_ticks() - bullet.attack_time > bullet.attack_duration:
                bullet.kill()

        self.thunder_hits.update()
        for thunder in self.thunder_hits:
            thunder.draw(surface, offset)
            if pygame.time.get_ticks() - thunder.attack_time > thunder.attack_duration and thunder.attack == True:
                thunder.kill()

    def check_damage(self, player, enemies):
        # Hit groups:
        sword_collisions = []
        arrow_collisions = []
        thunder_collisions = []
        def character_kill(character) -> None:
            character.dead = True
            character.status = 'dead'
            character.frame_index = 0
            character.direction.x = 0
            character.dead_time = pygame.time.get_ticks()

            if character.type != 'player':
                player.add_experience(character.experience)

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
                    if hit.rect.colliderect(enemy.collision_rect) and hit.source == 'player' and enemy.dead == False: # If enemy get hit by player
                        if kind == 'thunder' and hit.attack == False: break
                        elif kind == 'thunder' and hit.attack == True and player.id in hit.character_collided: break
                        else:
                            collisions_group.append((enemy, hit.damage, hit.source))
                            hit.character_collided.append(enemy.id)
                            if kind == 'bullet': point = True


                if hit.rect.colliderect(player.movement.collision_rect) and not hit.shielded and hit.source != 'player' and player.dead == False: # If player get hit by enemy
                    for enemy in enemies:
                        if enemy.id == hit.source_id:
                            if kind == 'thunder':
                                if hit.attack == False:
                                    break
                                elif hit.attack == True and player.id in hit.character_collided:
                                    break
                                elif hit.attack == True and player.id not in hit.character_collided:
                                    hit.character_collided.append(player.id)
                                    collisions_group.append((player, hit.damage, hit.source))
                                    break
                            if player.shielding:
                                if ((player.facing_right and enemy.collision_rect.x > player.movement.collision_rect.x) or
                                    (not player.facing_right and enemy.collision_rect.x < player.movement.collision_rect.x)):
                                    self.shield_block_sound.play()
                                    hit.shielded = True
                                    print('Zablokowano')
                                    if not enemy.stunned and kind == 'sword':
                                        print('Zestunowano')
                                        enemy.frame_index = 0
                                        enemy.direction.x = 0
                                        enemy.stunned = True
                                        enemy.status = 'stun'
                                        enemy.armor_ratio = 3
                                        break
                                else:
                                    hit.character_collided.append(player.id)
                                    collisions_group.append((player, hit.damage, hit.source))
                            else:
                                hit.character_collided.append(player.id)
                                collisions_group.append((player, hit.damage, hit.source))
                    if kind == 'bullet': point = True

                if point and kind == 'bullet': # Destroy bullet after collision with anyone
                    hit.kill()
        def character_hit_collisions(collisions) -> None:
            if collisions:  # If there is attack collision with enemies:
                for collision in collisions:
                    character = collision[0]
                    damage = collision[1]
                    source = collision[2].lower()

                    if not character.just_hurt and character.type.lower() != 'player' and source == 'player':
                        character_hurt(character, damage)
                    if not character.just_hurt and character.type.lower() == 'player' and source != 'player':
                        character_hurt(character, damage)

        character_search_hit_collisions('sword', self.sword_hits, player, enemies, sword_collisions)
        character_hit_collisions(sword_collisions)

        character_search_hit_collisions('bullet', self.bullet_hits, player, enemies, arrow_collisions)
        character_hit_collisions(arrow_collisions)

        character_search_hit_collisions('thunder', self.thunder_hits, player, enemies, thunder_collisions)
        character_hit_collisions(thunder_collisions)