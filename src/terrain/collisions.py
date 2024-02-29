def check_collisions(character_movement, sprites):
    """
    This function checks horizontal and vertical collisions of character with terrain sprites

    :param character_movement: movement object of character
    :param sprites: the nearest character sprites
    :return: none
    """
    horizontal_movement_collision(character_movement, sprites)
    vertical_movement_collision(character_movement, sprites)


def horizontal_movement_collision(character, sprites):
    """
    This function checks horizontal collisions of character with terrain sprites

    :param character: movement object of character
    :param sprites: the nearest character sprites
    :return: none
    """
    character.collision_rect.x += character.direction.x * character.speed
    collidable_sprites = sprites.sprites()

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


def vertical_movement_collision(character, sprites):
    """
    This function checks vertical collisions of character with terrain sprites

    :param character: movement object of character
    :param sprites: the nearest character sprites
    :return: none
    """
    character.apply_gravity()
    collidable_sprites = sprites.sprites()

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
