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
