# крч чтобы не сливалось, не закрашивать захваченный оазис целиком, а просто ставить крестик определенного цвета

import pygame
from game.game_elements.elements import *


cell_size = 20


def draw_cell(screen, cell):
    if cell.cell_type == CellType.wall:
        pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size),
        )
    elif cell.cell_type == CellType.oases:
        pygame.draw.rect(
            screen,
            pygame.Color("orange"),
            (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size),
            5,
        )
    elif cell.cell_type == CellType.oases_pl_1:
        pygame.draw.rect(
            screen,
            pygame.Color("red"),
            (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size),
        )
    elif cell.cell_type == CellType.oases_pl_2:
        pygame.draw.rect(
            screen,
            pygame.Color("green"),
            (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size),
        )
    elif cell.cell_type == CellType.empty:
        pygame.draw.rect(
            screen,
            pygame.Color("grey"),
            (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size),
            1,
        )
    else:
        # вызвать исключение???
        return


def draw_player(screen, player):
    # хммм добавить пунктир по контуру фигуры?
    center_step = cell_size // 2
    radius = cell_size // 3
    if player.pl_numb == 0:
        pygame.draw.circle(
            screen,
            pygame.Color("red"),
            (player.x * cell_size + center_step, player.y * cell_size + center_step),
            radius,
            6,
        )
    elif player.pl_numb == 1:
        pygame.draw.circle(
            screen,
            pygame.Color("green"),
            (player.x * cell_size + center_step, player.y * cell_size + center_step),
            radius,
            6,
        )


def print_img(dict_elements) -> None:
    """

    :param dict_elements:
    :return:
    """

    n_cols = len(dict_elements["cells"][0])
    n_rows = len(dict_elements["cells"])

    width = n_cols * cell_size
    height = n_rows * cell_size

    # создадим экран
    screen = pygame.display.set_mode((width, height))

    # отрисуем ячейки
    for cell_l in dict_elements["cells"]:
        for cell in cell_l:
            draw_cell(screen, cell)

    # поверх ячеек отрисуем игроков
    pl_1 = dict_elements["players"][0]
    pl_2 = dict_elements["players"][1]
    draw_player(screen, pl_1)
    draw_player(screen, pl_2)

    pygame.image.save(screen, f"screens/img_{pl_1.pl_name}_{pl_2.pl_name}.jpg")
