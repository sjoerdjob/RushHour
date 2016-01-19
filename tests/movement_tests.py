from nose.tools import assert_raises_regexp, eq_
import unittest

from rushhour.board import Car
from rushhour.board import Direction
from rushhour.board import InvalidMoveError
from rushhour.board import board_from_string


class MovementTests(unittest.TestCase):
    def setUp(self):
        self.red_car = Car('r', Direction.horizontal, 2)
        self.board = board_from_string("""\
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
""")

    def _find_car(self, color):
        for car in self.board.cars:
            if car.color == color:
                return car
        raise ValueError("Car not found")

    def test_setup(self):
        eq_(self.board.car_at_position(0, 2), self.red_car)
        eq_(self.board.car_at_position(2, 2), None)

    def test_valid_horizontal_move(self):
        self.board.move(self.red_car, Direction.horizontal, 1)
        eq_(self.board.car_at_position(0, 2), None)
        eq_(self.board.car_at_position(2, 2), self.red_car)

    def test_move_out_of_binds(self):
        with assert_raises_regexp(InvalidMoveError, ".*bounds.*"):
            self.board.move(self.red_car, Direction.horizontal, -1)

    def test_moving_to_the_side(self):
        with assert_raises_regexp(InvalidMoveError, ".*side.*"):
            self.board.move(self.red_car, Direction.vertical, -1)

    def test_buming_into_a_car(self):
        with assert_raises_regexp(InvalidMoveError, ".*bump.*"):
            self.board.move(self.red_car, Direction.horizontal, 4)

    def test_solve_sequence(self):
        self.board.move(self._find_car('A'), Direction.horizontal, -4)
        self.board.move(self._find_car('B'), Direction.horizontal, -2)
        self.board.move(self._find_car('C'), Direction.horizontal, -2)
        self.board.move(self._find_car('E'), Direction.vertical, -2)
        self.board.move(self._find_car('F'), Direction.vertical, -2)
        self.board.move(self._find_car('H'), Direction.horizontal, 2)
        self.board.move(self._find_car('I'), Direction.vertical, -1)
        self.board.move(self._find_car('J'), Direction.horizontal, -3)
        self.board.move(self._find_car('I'), Direction.vertical, 1)
        self.board.move(self._find_car('H'), Direction.horizontal, -2)
        self.board.move(self._find_car('E'), Direction.vertical, 3)
        self.board.move(self._find_car('F'), Direction.vertical, 3)
        self.board.move(self._find_car('r'), Direction.horizontal, 4)

        # Check that the red car is at the finish line.
        eq_(self.board.car_at_position(5, 2), self.red_car)
