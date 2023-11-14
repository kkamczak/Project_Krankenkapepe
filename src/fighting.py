"""
fighting.py - Module for managing combat-related classes and functionality.

This module contains classes for handling combat-related elements such as
attacks, hits, and damage calculation in a game.

Classes:
    - Hit: Represents a melee hit in the game.
    - Bullet: Represents a ranged attack projectile.
    - Thunder: Represents a powerful area-of-effect attack.
    - Fight_Manager: Manages and handles combat-related interactions.

"""
import pygame
from settings import YELLOW, RED, PLAYER_ATTACK_SIZE, SHOW_HIT_RECTANGLES, BULLET_DEFAULT_SPEED, \
    SCREEN_HEIGHT, ENEMY_ATTACK_SIZE

class Hit(pygame.sprite.Sprite):
    """
    Represents a melee hit in the game.

    This class is used to create and manage melee hits during combat.

    Methods:
        - update(): Update the hit's state.
            This method updates the state of the hit, but for melee hits,
            there is no additional logic needed in the update function.

        - draw(surface, offset): Draw the hit on a surface with an offset.
            This method is responsible for drawing the hit's visual representation
            on the provided surface with the given offset.

    """
    def __init__(self, pos, damage, source, source_id):
        """
        Initialize a melee hit instance.

        Args:
            pos (tuple): The position where the hit occurs.
            damage (int): The amount of damage the hit deals.
            source (str): The source of the hit (e.g., 'player' or 'enemy').
            source_id (int): The unique identifier of the source.
        """
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
        """
           Update the melee hit's state.
        """
        pass
    def draw(self, surface, offset):
        """
        Draw the melee hit on a surface with an offset.

        Args:
            surface (pygame.Surface): The surface on which to draw the hit.
            offset (tuple): The offset to apply to the hit's position.
        """
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)


class Bullet(pygame.sprite.Sprite):
    """
    Represents a ranged attack projectile.

    This class is used to create and manage ranged attack projectiles.

    Methods:
        - update(): Update the projectile's position and state.
            This method updates the position and state of the projectile based on its
            direction and speed. It also handles collision detection and destruction
            of the projectile if it reaches its maximum duration.

        - draw(surface, offset): Draw the projectile on a surface with an offset.
            This method is responsible for drawing the projectile's visual representation
            on the provided surface with the given offset.

    """
    def __init__(self, kind, pos, damage, source, source_id, facing_right):
        """
        Initialize a ranged attack projectile.

        Args:
            kind (str): The type of projectile (e.g., 'arrow' or 'bullet').
            pos (tuple): The starting position of the projectile.
            damage (int): The amount of damage the projectile deals.
            source (str): The source of the projectile (e.g., 'player' or 'enemy').
            source_id (int): The unique identifier of the source.
            facing_right (bool): Indicates the direction of the projectile.
        """
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
        """
           Update the projectile's position and state.

        """
        self.collision_rect.x += self.direction.x * self.speed
        if self.facing_right:
            self.rect.topright = self.collision_rect.topright
            self.rect = self.image.get_rect(topright=self.rect.topright)
        else:
            self.rect.topleft = self.collision_rect.topleft
            self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def draw(self, surface, offset):
        """
        Draw the projectile on a surface with an offset.
        """
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)


class Thunder(pygame.sprite.Sprite):
    """
    Represents a powerful area-of-effect attack.

    This class is used to create and manage area-of-effect attacks, such as thunderstorms.

    Methods:
        - update(): Update the attack area.
            This method updates the attack area's position and size as it shrinks over time.
            It also handles the activation and deactivation of the attack.

        - draw(surface, offset): Draw the attack area on a surface with an offset.
            This method is responsible for drawing the attack area's visual representation
            on the provided surface with the given offset.

    """
    def __init__(self, pos, damage, source, source_id):
        """
        Initialize an area-of-effect attack (thunderstorm).

        Args:
            pos (pygame.Rect): The area where the thunderstorm occurs.
            damage (int): The amount of damage the attack deals.
            source (str): The source of the attack (e.g., 'player' or 'enemy').
            source_id (int): The unique identifier of the source.
        """
        super().__init__()
        self.source = source
        self.source_id = source_id

        self.width = 60
        self.height = 1500
        self.position = [pos.centerx - self.width/2, pos.bottom-SCREEN_HEIGHT]

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)
        self.image.set_alpha(30)

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
        """
        Update the attack area (thunderstorm).
        """
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
        """
        Draw the attack area (thunderstorm) on a surface with an offset.
        """
        pos = self.rect.topleft - offset
        surface.blit(self.image, pos)


class Fight_Manager():
    """
    Manages and handles combat-related interactions.

    This class manages combat-related interactions,
    including hits, projectiles, and damage calculations.

    Methods:
        - sword_attack(character): Perform a sword attack.

        - arch_attack(kind, character): Perform an archery attack.

        - thunder_attack(source, source_id, position, damage, can_attack):
        Perform a thunder attack.

        - attack_update(surface, offset): Update combat-related elements.

        - check_damage(player, enemies): Check and apply damage to characters.

    """
    def __init__(self):
        """
        Initialize the Fight_Manager instance.

        This class manages combat-related interactions, including hits, projectiles, and damage calculations.
        """
        # Fighting:
        self.sword_hits = pygame.sprite.Group()
        self.bullet_hits = pygame.sprite.Group()
        self.thunder_hits = pygame.sprite.Group()

        # Sounds:
        self.shield_block_sound = pygame.mixer.Sound('content/sounds/character/shield_block.mp3')
        self.shield_block_sound.set_volume(0.05)
    def sword_attack(self, character):
        """
        Perform a sword attack.

        Args:
            character: The character performing the sword attack.

        This method creates and manages a sword attack based on the character's parameters,
        including position, direction, and damage.
        """
        attack = character.fighting.attack
        rect = character.movement.collision_rect
        if attack['able'] or (character.status.type == 'player' and attack['attacking']):
            if character.status.facing_right:
                position = (
                    rect.centerx + attack['space'],
                    rect.bottom - attack['size'][1]
                )
            else:
                position = (
                    rect.centerx - rect.width - attack['space'],
                    rect.bottom - attack['size'][1]
                )

            hit = Hit(position, attack['damage'], character.status.type, character.status.id)
            self.sword_hits.add(hit)

    def arch_attack(self, kind, character):
        """
        Perform an archery attack (e.g., arrows).

        Args:
            kind (str): The type of archery attack (e.g., 'arrow').
            character: The character performing the archery attack.

        This method creates and manages an archery attack based on the character's parameters,
        including position, direction, and damage.
        """
        if character.status.type == 'player':
            attack = character.fighting.arch
        else:
            attack = character.fighting.attack
        rect = character.movement.collision_rect
        if attack['able'] or (character.status.type == 'player' and attack['attacking']):
            if character.status.facing_right:
                position = (rect.right, rect.top + rect.height / 3)
            else:
                position = (rect.left + 20, rect.top + rect.height / 3)
            bullet = Bullet(
                kind, position, attack['damage'],
                character.status.type, character.status.id,
                character.status.facing_right
            )
            self.bullet_hits.add(bullet)

    def thunder_attack(self, source, source_id, position, damage, can_attack):
        """
        Perform a thunderstorm attack.

        Args:
            source (str): The source of the attack (e.g., 'player' or 'enemy').
            source_id (int): The unique identifier of the source.
            position (pygame.Rect): The position of the thunderstorm.
            damage (int): The amount of damage the attack deals.
            can_attack (bool): Indicates whether the attack can be performed.

        This method creates and manages a thunderstorm attack based on the provided parameters.
        """
        if can_attack:
            thunder = Thunder(position, damage, source, source_id)
            self.thunder_hits.add(thunder)

    def attack_update(self, surface, offset: pygame.Vector2):
        """
        Update combat-related elements.

        Args:
            surface (pygame.Surface): The surface on which to update combat elements.
            offset (pygame.Vector2): The offset to apply to combat elements' positions.

        This method updates the state and position of melee hits,
        projectiles, and area-of-effect attacks.
        It also handles the removal of expired attacks.
        """
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
            if pygame.time.get_ticks() - thunder.attack_time > thunder.attack_duration and thunder.attack is True:
                thunder.kill()

    def check_damage(self, player, enemies):
        """
        Check and apply damage to characters.

        Args:
            player: The player character.
            enemies: A list of enemy characters.

        This method checks for collisions between attacks and characters, calculates damage,
        and applies damage to characters accordingly.
        It also handles experience points and character status updates.
        """
        # Hit groups:
        sword_collisions = []
        arrow_collisions = []
        thunder_collisions = []

        self.character_search_hit_collisions('sword', self.sword_hits, player, enemies, sword_collisions)
        self.character_hit_collisions(sword_collisions, player)

        self.character_search_hit_collisions('bullet', self.bullet_hits, player, enemies, arrow_collisions)
        self.character_hit_collisions(arrow_collisions, player)

        self.character_search_hit_collisions('thunder', self.thunder_hits, player, enemies, thunder_collisions)
        self.character_hit_collisions(thunder_collisions, player)

    def character_search_hit_collisions(self, kind, hits, player, enemies, collisions_group) -> None:
        """
        Check and handle collisions between hits and characters.

        This method checks for collisions between hits and characters, such as enemies and the player.
        It calculates and records damage and manages various hit conditions and interactions.
        """
        for hit in hits:  # Check for any hits collisions
            point = False  # if kind of hits is 'bullets'
            for enemy in enemies:
                if hit.rect.colliderect(enemy.movement.collision_rect) and \
                        hit.source == 'player' and \
                        not enemy.properties.dead['status']:  # If enemy get hit by player
                    if kind == 'thunder' and hit.attack is False:
                        break
                    elif kind == 'thunder' and hit.attack is True and player.status.id in hit.character_collided:
                        break
                    else:
                        collisions_group.append((enemy, hit.damage, hit.source))
                        hit.character_collided.append(enemy.status.id)
                        if kind == 'bullet': point = True

            if hit.rect.colliderect(player.movement.collision_rect) and \
                    not hit.shielded and \
                    hit.source != 'player' and \
                    not player.properties.dead['status']:  # If player get hit by enemy
                for enemy in enemies:
                    if enemy.status.id != hit.source_id:
                        continue
                    if kind == 'thunder':
                        if hit.attack is False:
                            break
                        if hit.attack is True and player.status.id in hit.character_collided:
                            break
                        if hit.attack is True and player.status.id not in hit.character_collided:
                            hit.character_collided.append(player.status.id)
                            collisions_group.append((player, hit.damage, hit.source))
                            break
                    if player.defense.shield['shielding']:
                        if ((player.status.facing_right and enemy.movement.collision_rect.x > player.movement.collision_rect.x) or
                            (not player.status.facing_right and enemy.movement.collision_rect.x < player.movement.collision_rect.x)):
                            self.shield_block_sound.play()
                            hit.shielded = True
                            if not enemy.fighting.combat['stunned'] and kind == 'sword':
                                enemy.animations.frame_index = 0
                                enemy.movement.direction.x = 0
                                enemy.fighting.combat['stunned'] = True
                                enemy.status.status = 'stun'
                                enemy.defense.armor_ratio = 3
                                break
                        else:
                            hit.character_collided.append(player.status.id)
                            collisions_group.append((player, hit.damage, hit.source))
                    else:
                        hit.character_collided.append(player.status.id)
                        collisions_group.append((player, hit.damage, hit.source))
                if kind == 'bullet': point = True

            if point and kind == 'bullet':  # Destroy bullet after collision with anyone
                hit.kill()

    def character_hit_collisions(self, collisions, player) -> None:
        """
        Handle character hit collisions and apply damage.

        This method handles the results of character hit collisions, including applying damage to characters.
        It also handles experience point updates and character status changes.
        """
        if collisions:  # If there is attack collision with enemies:
            for collision in collisions:
                character = collision[0]
                damage = collision[1]
                source = collision[2].lower()

                if not character.defense.just_hurt and character.status.type.lower() != 'player' and source == 'player':
                    if character.defense.hurt(damage):
                        player.properties.add_experience(character.properties.experience['current'])
                if not character.defense.just_hurt and character.status.type.lower() == 'player' and source != 'player':
                    character.defense.hurt(damage)
