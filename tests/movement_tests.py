from nose.tools import eq_
import unittest

from rushhour.board import Car
from rushhour.board import Direction
from rushhour.board import board_from_string


class MovementTests(unittest.TestCase):
    def setUp(self):
        self.board = board_from_string("""\
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
""")

    def test_valid_horizontal_move(self):
        red_car = Car('r', Direction.horizontal, 2)
        eq_(self.board.car_at_position(0, 2), red_car)
        eq_(self.board.car_at_position(2, 2), None)
        self.board.move(red_car, Direction.horizontal, 1)
        eq_(self.board.car_at_position(0, 2), None)
        eq_(self.board.car_at_position(2, 2), red_car)
