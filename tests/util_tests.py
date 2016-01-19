from nose.tools import eq_

from rushhour._util import TransposedView


def test_transposed_view():
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    transposed = TransposedView(grid)

    eq_(grid[0][2], 3)
    eq_(transposed[2][0], 3)
    
    grid[1][2] = 9
    eq_(transposed[2][1], 9)

    transposed[1][2] = 9
    eq_(grid[2][1], 9)
