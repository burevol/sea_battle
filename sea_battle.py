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


class Ship:
    def __init__(self, length, rostrum, orientation, lives):
        self.length = length
        self.rostrum = rostrum
        self.orientation = orientation
        self.lives = lives

        if self.orientation == HORIZONTAL:
            self.dots = [Dot(rostrum.x, j) for j in range(rostrum.y, rostrum.y + lives)]
        elif self.orientation == VERTICAL:
            self.dots = [Dot(i, rostrum.y) for i in range(rostrum.x, rostrum.x + lives)]
        else:
            raise ValueError("Неверный тип ориентации.")

    def dots(self):
        return self.dots


class Board:
    def __init__(self, hidden):
        self._board = [[CLEAR for x in range(0, 6)] for y in range(0, 6)]
        self.ships = []
        self.hidden = hidden
        self.ships_active = 0

    def add_ship(self, ship):
        pass

    def contour(self, ship):
        pass

    def print_board(self):
        pass

    @staticmethod
    def out(self, dot):
        if 1 <= dot.x <= 6 and 1 <= dot.y <= 6:
            return True
        else:
            return False

    def shot(self, x, y):
        pass

