def horizontal_movement_collision(character, sprites):
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