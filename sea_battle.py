from random import randrange, choice

HORIZONTAL = 1
VERTICAL = 2
CLEAR = '0'
SHIP = '▄'
HIT = 'X'
MISS = 'T'


class CellAlreadyUsedException(Exception):
    pass


class BoardOutException(Exception):
    pass


class OrientationTypeException(Exception):
    pass


class CannotPlaceShipException(Exception):
    pass


class WrongInputException(Exception):
    pass


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
            raise OrientationTypeException

    @property
    def dots(self):
        return self._dots


class Board:
    def __init__(self, hidden):
        self._board = [[CLEAR for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.hidden = hidden
        self.ships_active = 0
        self.contours_dots = []

    def add_ship(self, ship):
        for dot in ship.dots:
            if Board.out(dot):
                raise BoardOutException("Корабль выходит за границы карты")
            elif dot in self.contours_dots:
                raise CellAlreadyUsedException()
            for map_ship in self.ships:
                if dot in map_ship.dots:
                    raise CellAlreadyUsedException()
        self.ships.append(ship)
        self.ships_active += 1
        self.contours_dots.extend(self.contour(ship))
        if not self.hidden:
            for dot in ship.dots:
                self._board[dot.x][dot.y] = SHIP

    @staticmethod
    def contour(current_ship):

        # TODO вынести current_ship.rostrum в отдельную переменнуюы
        contour_dots = []
        if current_ship.orientation == HORIZONTAL:
            for y in range(current_ship.rostrum.y - 1, current_ship.rostrum.y + current_ship.length + 1):
                contour_dots.append(Dot(current_ship.rostrum.x - 1, y))
                contour_dots.append(Dot(current_ship.rostrum.x + 1, y))
            contour_dots.append(Dot(current_ship.rostrum.x, current_ship.rostrum.y - 1))
            contour_dots.append(Dot(current_ship.rostrum.x, current_ship.rostrum.y + current_ship.length))
        elif current_ship.orientation == VERTICAL:
            for x in range(current_ship.rostrum.x - 1, current_ship.rostrum.x + current_ship.length + 1):
                contour_dots.append(Dot(x, current_ship.rostrum.y - 1))
                contour_dots.append(Dot(x, current_ship.rostrum.y + 1))
            contour_dots.append(Dot(current_ship.rostrum.x - 1, current_ship.rostrum.y))
            contour_dots.append(Dot(current_ship.rostrum.x + current_ship.length, current_ship.rostrum.y))
        else:
            raise OrientationTypeException()

        return list(filter(lambda dot: not Board.out(dot), contour_dots))

    def print_board(self):
        print(' |1|2|3|4|5|6|')
        for i, row in enumerate(self._board):
            print(f'{i + 1}|{"|".join(row)}|')

    @staticmethod
    def out(dot):
        if 0 <= dot.x <= 5 and 0 <= dot.y <= 5:
            return False
        else:
            return True

    def shot(self, dot):
        pass


class Player:
    def __init__(self, board1, board2):
        self.my_board = board1
        self.enemy_board = board2
        self.turns = []

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                dot = self.ask()
            except WrongInputException:
                print('Неправильный ввод, повторите')
            else:
                self.enemy_board.shot(dot)


class AI(Player):

    def ask(self):
        can_exit = False
        target = None

        while not can_exit:
            target = Dot(randrange(6), randrange(6))
            if target not in self.turns:
                can_exit = True

        return target


class User(Player):
    def ask(self):
        s = input("Введите координаты хода:")
        m = s.split()
        if len(m) != 2:
            raise WrongInputException()
        if not m[0].isdigit() or not m[1].isdigit():
            raise WrongInputException()
        x, y = int(m[0]), int(m[1])
        dot = Dot(x, y)
        if Board.out(dot):
            raise WrongInputException()
        return dot


class Game:
    @staticmethod
    def random_board(hidden):
        while True:
            generated_board = Board(hidden)
            try:
                Game.add_ship_to_board(generated_board, 3)
                for _ in range(2):
                    Game.add_ship_to_board(generated_board, 2)
                for _ in range(4):
                    Game.add_ship_to_board(generated_board, 1)

            except CannotPlaceShipException:
                pass
            else:
                return generated_board

    @staticmethod
    def add_ship_to_board(player_board, length):
        for i in range(10000):
            try:
                player_board.add_ship(
                    Ship(length, Dot(randrange(6), randrange(6)), choice((HORIZONTAL, VERTICAL))))
            except BoardOutException:
                pass
            except CellAlreadyUsedException:
                pass
            else:
                break
        else:
            raise CannotPlaceShipException()

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
    game_board = Game.random_board(False)
    game_board.print_board()
# ship = Ship(1, Dot(1, 1), HORIZONTAL)
# contour = Board.contour(ship)
# for dot in contour:
#    print(str(dot))
