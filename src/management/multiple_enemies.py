from pygame.surface import Surface
from pygame.math import Vector2
from tools.support import draw_text
from tools.settings import FONT_SMALL, RED


def show_multiple_enemies(enemies: list, screen: Surface, distance: int, offset: Vector2) -> None:
    """
    This function displays information if several opponents are overlapped.

    :param enemies: group of enemies
    :param screen: display screen
    :param distance: distance to calculate
    :param offset: offset of camera
    :return: none
    """
    if len(enemies) < 2:
        return

    max_distance = distance
    nearest_distance = distance
    nearest_left = None
    nearest_right = None

    for enemy in enemies:
        rect = enemy.movement.collision_rect
        for other_enemy in enemies:
            other_rect = other_enemy.movement.collision_rect
            if enemy != other_enemy:
                distance_x = abs(rect.centerx - other_rect.centerx)
                distance_y = abs(rect.centery - other_rect.centery)
                if distance_x < max_distance and distance_y < max_distance and distance_x < nearest_distance:
                    nearest_distance = distance_x
                    nearest_left = enemy if rect.x < other_rect.x else other_enemy
                    nearest_right = other_enemy if other_rect.x < rect.x else enemy

    if nearest_left and nearest_right:
        rect_r = nearest_right.movement.collision_rect
        rect_l = nearest_left.movement.collision_rect
        middle_x = (rect_r.centerx + rect_l.centerx) / 2
        middle_y = (rect_r.centery + rect_l.centery) / 2

        enemies_within_radius = sum(1 for enemy in enemies if abs(enemy.movement.collision_rect.centerx - middle_x) < max_distance)
        draw_text(screen, f'{enemies_within_radius}', FONT_SMALL, RED, middle_x - offset.x, middle_y - offset.y - 100, left=True)
