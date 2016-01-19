from nose.tools import assert_in, eq_

from rushhour.board import _car_from_positions
from rushhour.board import board_from_string
from rushhour.board import Car


def test_car_from_horizontal_positions1():
    position, car = _car_from_positions('r', {(0, 0), (1, 0)})
    eq_(car.color, 'r')
    eq_(car.orientation, Car.HORIZONTAL)
    eq_(car.length, 2)
    eq_(position, (0, 0))


def test_car_from_horizontal_positions2():
    position, car = _car_from_positions('r', {(2, 5), (3, 5), (4, 5)})
    eq_(car.color, 'r')
    eq_(car.orientation, Car.HORIZONTAL)
    eq_(car.length, 3)
    eq_(position, (2, 5))


def test_car_from_vertical_positions1():
    position, car = _car_from_positions('r', {(0, 0), (0, 1), (0, 2)})
    eq_(car.color, 'r')
    eq_(car.orientation, Car.VERTICAL)
    eq_(car.length, 3)
    eq_(position, (0, 0))


def test_load_empty_board():
    board_description = """\
......
......
......
......
......
......
"""

    board = board_from_string(board_description)
    
    eq_(len(board.cars), 0)


def test_load_board_with_only_red_car():
    board_description = """\
......
rr....
......
......
......
......
"""

    board = board_from_string(board_description)
    
    eq_(len(board.cars), 1)
    assert_in(Car('r', Car.HORIZONTAL, 2), board.cars)


def test_load_complex_board():
    board_description = """\
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
"""

    board = board_from_string(board_description)

    eq_(len(board.cars), 10)
    assert_in(Car('r', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('A', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('B', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('C', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('E', Car.VERTICAL, 3), board.cars)
    assert_in(Car('F', Car.VERTICAL, 3), board.cars)
    assert_in(Car('G', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('H', Car.HORIZONTAL, 2), board.cars)
    assert_in(Car('I', Car.VERTICAL, 2), board.cars)
    assert_in(Car('J', Car.HORIZONTAL, 2), board.cars)
