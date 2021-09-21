from random import randrange, choice

HORIZONTAL = 1
VERTICAL = 2
CLEAR = 'О'
SHIP = '▄'
HIT = 'X'
MISS = 'T'


class CellAlreadyUsedException(Exception):
    pass


class BoardOutException(Exception):
    pass


class CannotPlaceShipException(Exception):
    pass


class WrongInputException(Exception):
    pass


class WinException(Exception):
    pass


class WrongPointToShipException(Exception):
    pass


class QuitException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x + 1}, {self.y + 1})'  # транслируем в систему координат доски


class Ship:
    def __init__(self, length, head, orientation):
        self.length = length
        self.head = head
        self.orientation = orientation
        self.lives = length

        if self.orientation == HORIZONTAL:
            self._dots = [Dot(head.x, j) for j in range(head.y, head.y + length)]
        elif self.orientation == VERTICAL:
            self._dots = [Dot(i, head.y) for i in range(head.x, head.x + length)]

    @property
    def dots(self):
        return self._dots

    def hit(self, dot):
        if dot not in self.dots:
            raise WrongPointToShipException('Критическая ошибка при расчете координат')
        self.lives -= 1
        return True if not self.lives else False


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
                raise CellAlreadyUsedException("Точка корабля является соседней для уже существующего корабля")
            for map_ship in self.ships:
                if dot in map_ship.dots:
                    raise CellAlreadyUsedException("Точка пересекается с существующим кораблем")

        self.ships.append(ship)
        self.ships_active += 1
        self.contours_dots.extend(self.contour(ship))
        if not self.hidden:
            for dot in ship.dots:
                self._board[dot.x][dot.y] = SHIP

    @staticmethod
    def contour(current_ship):
        head_dot = current_ship.head
        contour_dots = []
        if current_ship.orientation == HORIZONTAL:
            for y in range(head_dot.y - 1, head_dot.y + current_ship.length + 1):
                contour_dots.append(Dot(head_dot.x - 1, y))
                contour_dots.append(Dot(head_dot.x + 1, y))
            contour_dots.append(Dot(head_dot.x, head_dot.y - 1))
            contour_dots.append(Dot(head_dot.x, head_dot.y + current_ship.length))
        elif current_ship.orientation == VERTICAL:
            for x in range(head_dot.x - 1, head_dot.x + current_ship.length + 1):
                contour_dots.append(Dot(x, head_dot.y - 1))
                contour_dots.append(Dot(x, head_dot.y + 1))
            contour_dots.append(Dot(head_dot.x - 1, head_dot.y))
            contour_dots.append(Dot(head_dot.x + current_ship.length, head_dot.y))

        return list(filter(lambda dot: not Board.out(dot), contour_dots))

    def print_board(self):
        print(' |1|2|3|4|5|6|')
        for i, row in enumerate(self._board):
            print(f'{i + 1}|{"|".join(row)}|')

    @staticmethod
    def out(dot):
        return not (0 <= dot.x <= 5 and 0 <= dot.y <= 5)

    def shot(self, dot):
        if Board.out(dot):
            raise BoardOutException()
        if self._board[dot.x][dot.y] == HIT or self._board[dot.x][dot.y] == MISS:
            raise CellAlreadyUsedException()
        for map_ship in self.ships:
            if dot in map_ship.dots:
                self._board[dot.x][dot.y] = HIT
                print("Попадание!")
                try:
                    if map_ship.hit(dot):
                        self.ships_active -= 1
                        print('Корабль уничтожен!')
                except WrongPointToShipException as exc:
                    raise RuntimeError(exc.args[0])

                return True

        self._board[dot.x][dot.y] = MISS
        print("Промах...")
        return False


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
                print('Неправильный ввод, повторите.')
            else:
                try:
                    result = self.enemy_board.shot(dot)
                except BoardOutException:
                    print("Координаты выходят за рамки поля, повторите ввод.")
                except CellAlreadyUsedException:
                    print('В данную точку уже был произведен выстрел.')
                else:
                    return result


class AI(Player):
    def ask(self):
        can_exit = False
        target = None

        while not can_exit:
            target = Dot(randrange(6), randrange(6))
            if target not in self.turns:
                can_exit = True

        print(f'Ход компьютера: {target}')
        self.turns.append(target)
        return target


class User(Player):
    def ask(self):
        self.draw_boards()
        s = input("Введите координаты хода:")
        if s == 'q':
            raise QuitException
        m = s.split()
        if len(m) != 2:
            raise WrongInputException()
        if not m[0].isdigit() or not m[1].isdigit():
            raise WrongInputException()
        x, y = int(m[0]), int(m[1])
        dot = Dot(x - 1, y - 1)
        if Board.out(dot):
            raise WrongInputException()
        return dot

    def draw_boards(self):
        print("Ваше игровое поле:")
        self.my_board.print_board()
        print('Игровое поле компьютера:')
        self.enemy_board.print_board()


class Game:
    def __init__(self):
        self.player_board = Game.random_board(False)
        self.ai_board = Game.random_board(True)
        self.player = User(self.player_board, self.ai_board)
        self.ai = AI(self.ai_board, self.player_board)

    @staticmethod
    def random_board(hidden):
        while True:
            generated_board = Board(hidden)
            len_ships = [3, 2, 2, 1, 1, 1, 1]
            try:
                for length in len_ships:
                    Game.add_ship_to_board(generated_board, length)

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
        print('|         введите "q" для выхода         |')
        print('------------------------------------------')

    def loop(self):
        win = False
        players = [self.player, self.ai]
        name_players = ["Игрок", "Компьютер"]
        current_player = 0
        while not win:
            while True:
                result = players[current_player].move()
                if players[current_player].enemy_board.ships_active == 0:
                    raise WinException(f"{name_players[current_player]} победил!")
                if not result:
                    break
            current_player = 1 if current_player == 0 else 0


    def start(self):
        self.greet()
        try:
            self.loop()
        except QuitException:
            print('Выход из игры.')
        except WinException as win:
            print(win.args[0])
        except RuntimeError as err:
            print(err.args[0])


if __name__ == "__main__":
    game = Game()
    game.start()
