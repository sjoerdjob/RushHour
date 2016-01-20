"""
Logic representing the board + pieces.
"""

from collections import defaultdict
from enum import Enum

from rushhour._util import SlottedDefaults, TransposedView


class InvalidCarError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class Direction(Enum):
    horizontal = 'horizontal'
    vertical = 'vertical'


class Board(object):
    def _blit(self, left, top, width, height, value):
        for offset_x in range(width):
            for offset_y in range(height):
                self._board[top + offset_y][left + offset_x] = value

    def __init__(self, positions_and_cars):
        self.cars = []
        self._board = [[None] * 6 for __ in range(6)]
        self._positions_by_car = {}
        for (pos_x, pos_y), car in positions_and_cars:
            self.cars.append(car)
            self._positions_by_car[car] = (pos_x, pos_y)
            self._blit(pos_x, pos_y, car.width, car.height, car)

    def copy(self):
        board = Board.__new__(Board)
        board.cars = self.cars[:]
        board._board = [row[:] for row in self._board]
        board._positions_by_car = self._positions_by_car.copy()
        return board

    def car_at_position(self, pos_x, pos_y):
        return self._board[pos_y][pos_x]

    def move(self, car, direction, count):
        assert car in self.cars
        pos_x, pos_y = self._positions_by_car[car]

        if car.orientation != direction:
            raise InvalidMoveError("Moving a car to the side? Please don't!")

        if direction == Direction.horizontal:
            pos, path = pos_x, self._board[pos_y]
        elif direction == Direction.vertical:
            pos, path = pos_y, TransposedView(self._board)[pos_x]
        else:
            raise ValueError("Invalid direction supplied.")

        if pos + count < 0 or pos + count + car.length > 6:
            # Yes, maybe the red car should be allowed to move outside the
            # board. However, an equivalent solution is to mark the game as won
            # as soon as the red car touches the right side of the board.
            raise InvalidMoveError("Car would go out of bounds")

        if count < 0:
            check_range = range(pos + count, pos)
        else:
            check_range = range(pos + car.length, pos + car.length + count)

        for idx in check_range:
            if path[idx] is not None:
                raise InvalidMoveError("Car would bump into other car.")

        for idx in range(pos, pos + car.length):
            path[idx] = None

        pos += count
        for idx in range(pos, pos + car.length):
            path[idx] = car

        if direction == Direction.horizontal:
            self._positions_by_car[car] = pos_x + count, pos_y
        elif direction == Direction.vertical:
            self._positions_by_car[car] = pos_x, pos_y + count

    @staticmethod
    def __count_prefix_nones(lst):
        for idx, val in enumerate(lst):
            if val is not None:
                return idx
        return len(lst)

    def get_moves(self):
        """
        Enumerates all possible moves at the current board.

        The return value will be a list of cars, directions, and min/max count.
        """
        moves = set()
        for car, position in self._positions_by_car.items():
            pos_x, pos_y = position
            if car.orientation == Direction.horizontal:
                path = self._board[pos_y]
                pos = pos_x
            else:
                path = TransposedView(self._board)[pos_x]
                pos = pos_y

            min_step = -self.__count_prefix_nones(list(reversed(path[0:pos])))
            max_step = self.__count_prefix_nones(path[pos + car.length:])
            for step in range(min_step, max_step + 1):
                if step != 0:
                    moves.add((car, car.orientation, step))

        return moves

    def __str__(self):
        return ''.join(
            ''.join(car.color if car else '.' for car in row) + "\n"
            for row in self._board
        )

    def is_victory(self):
        car_next_to_finish = self.car_at_position(5, 2)
        return car_next_to_finish and car_next_to_finish.color == 'r'

    def get_state(self):
        return tuple(
            car.color if car else '.' for row in self._board for car in row
        )


class Car(SlottedDefaults):
    __slots__ = ('color', 'orientation', 'length')

    def __init__(self, color, orientation, length):
        self.color = color
        self.orientation = orientation
        self.length = length

    @property
    def width(self):
        return self.length if self.orientation == Direction.horizontal else 1

    @property
    def height(self):
        return self.length if self.orientation == Direction.vertical else 1


def _car_from_positions(color, positions):
    if len(positions) <= 1:
        raise InvalidCarError("Cars should exist of more than 1 block")

    x_positions = [position[0] for position in positions]
    y_positions = [position[1] for position in positions]

    left, right = min(x_positions), max(x_positions)
    top, bottom = min(y_positions), max(y_positions)

    if top == bottom:
        orientation = Direction.horizontal
        size = right - left + 1
    elif left == right:
        orientation = Direction.vertical
        size = bottom - top + 1
    else:
        raise InvalidCarError("Car should only cover 1 row or 1 column")

    if len(positions) != size:
        raise InvalidCarError("Car should not have gaps")

    return (left, top), Car(color, orientation, size)


def board_from_string(string):
    positions_by_color = defaultdict(set)
    for row_idx, row in enumerate(string.splitlines()):
        for col_idx, val in enumerate(row):
            positions_by_color[val].add((col_idx, row_idx))
    # "." is not a color, but a placeholder for 'no car'.
    del positions_by_color['.']

    cars = []
    for color, positions in positions_by_color.items():
        cars.append(_car_from_positions(color, positions))
    return Board(cars)
