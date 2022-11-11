from game.game_elements.elements import *
from game.utils import *


class GameSession:
    # инициализируем игровую сетку
    # храним инфо о конкретной игровой сессии
    # следим за очередностью ходов игроков
    def __init__(self):
        # создать игровое поле
        self.gg = GameGrid()
        # создать игроков
        player_1 = Player("player_1")
        player_2 = Player("player_2", pl_numb=1)
        player_2.set_position(self.gg.n_cols - 1, self.gg.n_rows - 1)
        self.players = [player_1, player_2]
        # отрисовать имеющееся
        for_print_img = {"cells": self.gg.get_elements(), "players": self.players}
        print_img(for_print_img)

    def start_game_loop(self) -> None:
        """
        Крутимся в бесконечном цикле получения команд и выполнения шагов игроками, пока не получим
        исключение, свидетельствующее о победе одного из игроков или о невозможности продолжать игру
        :return:
        """

        curr_player = 0
        while True:
            commands = input()
            try:
                # НА КАЖДОМ ШАГЕ Я ДОЛЖЕН ПРОВЕРЯТЬ НЕ ПРОИСХОДИТ ЛИ У МЕНЯ ПЕРЕСЕЧЕНИЕ
                # С КАКИМИ-ЛИБО ИГРОВЫМИ ЭЛЕМЕНТАМИ И РЕАГИРОВАТЬ СООТВЕТСТВУЮЩИМ ОБРАЗОМ
                self.players[curr_player].series_steps(commands, self.gg.get_elements(), self.players[(curr_player + 1) % 2])
            except Exception as e:
                pass
            for_print_img = {"cells": self.gg.get_elements(), "players": self.players}
            print_img(for_print_img)

            # ПРОВЕРИТЬ у кого из игроков сколько захваченных баз

            self.gg.add_wall_block()
            curr_player = (curr_player + 1) % 2  # чтобы поочередно иметь значения 0 и 1


## ячейка с оазисом
### захвачена
### не захвачена
## ячейка со стеной
## пустая ячейка


if __name__ == "__main__":
    gs = GameSession()
    gs.start_game_loop()
