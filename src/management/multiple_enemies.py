from pygame.sprite import Group
from pygame.surface import Surface


def show_multiple_enemies(enemies: list, screen: Surface, distance: int) -> None:
    """
    This function displays information if several opponents are overlapped.

    :param enemies: group of enemies
    :param screen: display screen
    :param distance: distance to calculate
    :return: none
    """
    if len(enemies) < 2:
        return

    max_distance = distance
    nearest_distance = float('inf')
    nearest_left = None
    nearest_right = None

    for enemy in enemies:
        rect = enemy.movement.collision_rect
        for other_enemy in enemies:
            other_rect = other_enemy.movement.collision_rect
            if enemy != other_enemy:
                distance = rect.x - other_rect.x
                if distance < max_distance and distance < nearest_distance:
                    nearest_distance = distance
                    nearest_left = enemy if rect.x < other_rect.x else other_enemy
                    nearest_right = other_enemy if rect.x < other_rect.x else enemy

    if nearest_left and nearest_right:
        middle_point = (nearest_left.movement.collision_rect.x + nearest_right.movement.collision_rect.x) / 2
        enemies_within_radius = sum(1 for enemy in enemies if enemy.movement.collision_rect.x - middle_point < max_distance)
        print(f"Enemies in range {max_distance}: {enemies_within_radius}")
    else:
        print("Enemies not close")


