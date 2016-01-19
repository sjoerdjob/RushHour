from collections import defaultdict
from enum import Enum
from operator import itemgetter

from rushhour._util import SlottedDefaults


class InvalidCarError(Exception): pass


class Direction(Enum):
    horizontal = 'horizontal'
    vertical = 'vertical'


class Board(object):
    def _blit(self, left, top, width, height, value):
        for offset_x in range(width):
            for offset_y in range(height):
                self._board[left + offset_x][top + offset_y] = value

    def __init__(self, positions_and_cars):
        self.cars = []
        self._board = [[None] * 6 for __ in range(6)]
        self._positions_by_car = {}
        for (pos_x, pos_y), car in positions_and_cars:
            self.cars.append(car)
            self._positions_by_car[car] = (pos_x, pos_y)
            self._blit(pos_x, pos_y, car.width, car.height, car)

    def car_at_position(self, pos_x, pos_y):
        return self._board[pos_x][pos_y]

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

    x_positions = list(map(itemgetter(0), positions))
    y_positions = list(map(itemgetter(1), positions))

    top, bottom = min(y_positions), max(y_positions)
    left, right = min(x_positions), max(x_positions)

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
