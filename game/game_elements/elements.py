from enum import Enum
import random


class CellType(Enum):
    empty = 1
    wall = 2
    oases = 3  # только что инициализированный пустой оазис
    oases_pl_1 = 4  # оазес захвачен первым игроком
    oases_pl_2 = 5  # оазес захвачен вторым игроком


class BaseElement:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        assert x >= 0 and y >= 0, "Введено некорректное значение координаты элемента"
        assert isinstance(x, int) and isinstance(
            y, int
        ), "Координаты должны задаваться целочисленными значениями"
        self.x = x
        self.y = y

    def get_place(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}


class Cell(BaseElement):
    # ячейка
    def __init__(
        self, x: int = 0, y: int = 0, cell_type: CellType = CellType.empty
    ) -> None:
        """
        Ячейка игрового поля
        :param x:
        :param y:
        :param cell_type: тип ячейки
        """
        super().__init__(x, y)
        self.cell_type = cell_type

    def get_type(self) -> CellType:
        return self.cell_type

    def set_type(self, cell_type: CellType) -> None:
        self.cell_type = cell_type


class Player(BaseElement):
    # игрок
    def __init__(self, pl_name: str, pl_numb: int = 0, x: int = 0, y: int = 0) -> None:
        """
        Инициализация объекта игрок
        :param pl_name: уникальное имя игрока
        :param pl_numb: номер на игровом поле 0 или 1
        :param x: местоположение на оси X
        :param y: местоположение на оси Y
        """
        super().__init__(x, y)
        self.pl_name = pl_name
        self.pl_numb = pl_numb
        self.num_oases = 0  # число захваченных оазисов

    def step(self, direction: str, all_cells: list[list[Cell]], other_player):  #  -> dict[str, int]:
        """
        Один шаг в одну из сторон
        :param direction: l/r/u/d
        :return:
        """
        assert direction in ("l", "r", "u", "d"), "Некорректная команда для шага игрока"
        if direction == "l":
            self.x -= 1
        elif direction == "r":
            self.x += 1
        elif direction == "u":
            self.y -= 1
        elif direction == "d":
            self.y += 1

        # если при выполнении хотя бы одного step получим исключение выхода за границу, то вся последовательность
        # шагов должна откатиться

        # проверка на пересечение траектории с местоположением другого игрока
        if other_player.x == self.x and other_player.y == self.y:
            # raise ... здесь нужно самописное исключение
            return -2

        # проверка на выход за границы
        left_border, up_border = 0, 0
        right_border, down_border = len(all_cells[0]) - 1, len(all_cells) - 1
        if self.x < left_border or self.x > right_border:
            # raise ... здесь нужно кастомное самописное исключение
            return -1
        if self.y < up_border or self.y > down_border:
            # raise ...
            return -1

        # проверка на пересечение со стеной в центре
        # проверка на попадание в оазис
        for cell_l in all_cells:
            for cell in cell_l:
                if self.x == cell.x and self.y == cell.y:
                    if cell.cell_type  == CellType.wall:
                        # raise исключение, что наткнулись на стену
                        return -3
                    if cell.cell_type == CellType.oases:
                        if self.pl_numb == 0:
                            cell.cell_type = CellType.oases_pl_1
                        else:
                            cell.cell_type = CellType.oases_pl_2
                        # тут игроку надо добавить инфу о захваченном оазисе
                    if cell.cell_type == CellType.oases_pl_1:
                        if self.pl_numb == 1:
                            cell.cell_type = CellType.oases_pl_2
                    if cell.cell_type == CellType.oases_pl_2:
                        if self.pl_numb == 0:
                            cell.cell_type = CellType.oases_pl_1

        return {"x": self.x, "y": self.y}

    def series_steps(self, n_steps: str, all_cells: list[list[Cell]], other_player) -> dict[str, int]:
        assert len(n_steps) == 4, "Должно быть задано ровно 4 шага"
        curr_x = self.x
        curr_y = self.y
        for curr_step in n_steps:
            curr_info = self.step(curr_step, all_cells, other_player)
            if curr_info == -1:
                print("Некорректная последовательность шагов, выход за границы игрового поля")
                # производим откат изменений в позиции игрока, до исходной позиции
                self.x = curr_x
                self.y = curr_y
                break
            if curr_info == -2:
                print("Некорректная последовательность шагов, пересечение траектории с позицией другого игрока")
                # производим откат изменений в позиции игрока, до исходной позиции
                self.x = curr_x
                self.y = curr_y
                break
            if curr_info == -3:
                print("Некорректная последовательность шагов, пересечение траектории со стеной")
                # производим откат изменений в позиции игрока, до исходной позиции
                self.x = curr_x
                self.y = curr_y
                break
        return {"x": self.x, "y": self.y}

    def set_position(self, x: int, y: int) -> None:
        assert x >= 0 and y >= 0, "Введено некорректное значение координаты элемента"
        assert isinstance(x, int) and isinstance(
            y, int
        ), "Координаты должны задаваться целочисленными значениями"
        self.x = x
        self.y = y


class GameGrid:
    # игровое поле
    def __init__(self, n_cols: int = 39, n_rows: int = 29, n_oases: int = 8) -> None:
        assert n_cols > 1 and n_cols % 2 == 1, "Некорректное количество столбцов"
        assert n_rows > 1 and n_cols % 2 == 1, "Некорректное количество строк"
        assert isinstance(n_cols, int) and isinstance(
            n_rows, int
        ), "Ширина и высота должны быть целочисленными значениями"
        assert n_oases > 1 and n_oases % 2 == 0, "Некорректное количество оазисов"

        self.n_cols = n_cols
        self.n_rows = n_rows
        self.n_oases = n_oases

        # self.cells = np.array([[Cell(x, y) for x in range(self.n_cols)] for y in range(self.n_rows)])

        # создадим исходные ячейки
        self.cells = [
            [Cell(x, y) for x in range(self.n_cols)] for y in range(self.n_rows)
        ]

        # объявим ячейку - начало стены
        self.last_wall_idx_y = self.n_rows // 2
        self.cells[self.last_wall_idx_y][self.n_cols // 2].set_type(CellType.wall)
        self.n_wall = 1

        # объявим ячейки оазисы в случайных местах
        # чтобы в каждой половине карты их было поровну, и они не попадали на ячейки для стены и
        # на места появления игроков
        self.__set_random_oases()

    def add_wall_block(self) -> None:
        if self.n_wall >= self.n_rows:
            # raise ????
            return
        if self.n_wall % 2 == 1:
            self.last_wall_idx_y = self.last_wall_idx_y - self.n_wall
        else:
            self.last_wall_idx_y = self.last_wall_idx_y + self.n_wall

        self.cells[self.last_wall_idx_y][self.n_cols // 2].set_type(CellType.wall)
        self.n_wall += 1

    def __set_random_oases(self):
        left_cells = [
            self.cells[y][x]
            for y in range(0, self.n_rows)
            for x in range(0, self.n_cols // 2)
        ]
        left_cells_random = random.sample(left_cells[1:], self.n_oases // 2)
        for cell in left_cells_random:
            cell.set_type(CellType.oases)

        right_cells = [
            self.cells[y][x]
            for y in range(0, self.n_rows)
            for x in range(self.n_cols // 2 + 1, self.n_cols)
        ]
        right_cells_random = random.sample(
            right_cells[: len(right_cells) - 1], self.n_oases // 2
        )
        for cell in right_cells_random:
            cell.set_type(CellType.oases)

    def get_elements(self) -> list[list[Cell]]:
        return self.cells
