from nose.tools import assert_in, assert_raises_regexp, eq_

from rushhour.board import _car_from_positions
from rushhour.board import board_from_string
from rushhour.board import Car
from rushhour.board import Direction
from rushhour.board import InvalidCarError


def test_construct_too_small_car():
    with assert_raises_regexp(InvalidCarError, ".*more than 1 block.*"):
        _car_from_positions('r', {})
    with assert_raises_regexp(InvalidCarError, ".*more than 1 block.*"):
        _car_from_positions('r', {(0, 0)})


def test_construct_car_that_extends_beyond_one_line():
    with assert_raises_regexp(InvalidCarError, ".*1 row.*1 column.*"):
        _car_from_positions('r', {(0, 0), (1, 0), (0, 1)})


def test_construct_car_with_gaps():
    with assert_raises_regexp(InvalidCarError, ".*gaps.*"):
        _car_from_positions('r', {(0, 0), (0, 2)})


def test_car_from_horizontal_positions1():
    position, car = _car_from_positions('r', {(0, 0), (1, 0)})
    eq_(car.color, 'r')
    eq_(car.orientation, Direction.horizontal)
    eq_(car.length, 2)
    eq_(position, (0, 0))


def test_car_from_horizontal_positions2():
    position, car = _car_from_positions('r', {(2, 5), (3, 5), (4, 5)})
    eq_(car.color, 'r')
    eq_(car.orientation, Direction.horizontal)
    eq_(car.length, 3)
    eq_(position, (2, 5))


def test_car_from_vertical_positions1():
    position, car = _car_from_positions('r', {(0, 0), (0, 1), (0, 2)})
    eq_(car.color, 'r')
    eq_(car.orientation, Direction.vertical)
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
    assert_in(Car('r', Direction.horizontal, 2), board.cars)


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
    assert_in(Car('r', Direction.horizontal, 2), board.cars)
    assert_in(Car('A', Direction.horizontal, 2), board.cars)
    assert_in(Car('B', Direction.horizontal, 2), board.cars)
    assert_in(Car('C', Direction.horizontal, 2), board.cars)
    assert_in(Car('E', Direction.vertical, 3), board.cars)
    assert_in(Car('F', Direction.vertical, 3), board.cars)
    assert_in(Car('G', Direction.horizontal, 2), board.cars)
    assert_in(Car('H', Direction.horizontal, 2), board.cars)
    assert_in(Car('I', Direction.vertical, 2), board.cars)
    assert_in(Car('J', Direction.horizontal, 2), board.cars)


def test_get_car_at_position():
    board_description = """\
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
"""

    board = board_from_string(board_description)
    eq_(board.car_at_position(1, 2).color, 'r')
    eq_(board.car_at_position(4, 3).color, 'E')
    eq_(board.car_at_position(5, 5).color, 'J')
