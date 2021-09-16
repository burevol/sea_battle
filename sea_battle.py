from random import randrange

HORIZONTAL = 1
VERTICAL = 2
CLEAR = '0'
SHIP = '▄'
HIT = 'X'
MISS = 'T'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'x:{self.x}, y:{self.y}'


class Ship:
    def __init__(self, length, rostrum, orientation):
        self.length = length
        self.rostrum = rostrum
        self.orientation = orientation
        self.lives = length

        if self.orientation == HORIZONTAL:
            self._dots = [Dot(rostrum.x, j) for j in range(rostrum.y, rostrum.y + length)]
        elif self.orientation == VERTICAL:
            self._dots = [Dot(i, rostrum.y) for i in range(rostrum.x, rostrum.x + length)]
        else:
            raise ValueError("Неверный тип ориентации.")

    @property
    def dots(self):
        return self._dots


class Board:
    def __init__(self, hidden):
        self._board = [[CLEAR for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.hidden = hidden
        self.ships_active = 0

    def add_ship(self, ship):
        pass

    def contour(self, ship):
        pass

    def print_board(self):
        print(' |1|2|3|4|5|6|')
        for i, row in enumerate(self._board):
            print(f'{i+1}|{"|".join(row)}|')

    @staticmethod
    def out(dot):
        if 1 <= dot.x <= 6 and 1 <= dot.y <= 6:
            return True
        else:
            return False

    def shot(self, x, y):
        pass


class Player:
    def __init__(self, board1, board2):
        self.my_board = board1
        self.enemy_board = board2

    def ask(self):
        pass

    def move(self):
        pass


class AI(Player):
    pass


class User(Player):
    pass


class Game:
    def random_board(self):
        pass

    @staticmethod
    def greet():
        print('------------------------------------------')
        print('| Добро пожаловать в игру "Морской Бой". |')
        print('| Управление:                            |')
        print('|    Вводите координаты в формате: x y   |')
        print('|   x - номер  строки, y - номер столбца |')
        print('------------------------------------------')

    def loop(self):
        pass

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    board = Board(False)
    board.print_board()
