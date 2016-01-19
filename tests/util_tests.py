from nose.tools import assert_not_equals, eq_

from rushhour._util import SlottedDefaults
from rushhour._util import TransposedView


def slotted_defaults_test():
    class Test(SlottedDefaults):
        __slots__ = ("foo", "bar")
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    test_inst1 = Test("hello", "world")
    test_inst2 = Test("hello", "world")
    test_inst3 = Test("goodbye", "earth")

    eq_(repr(test_inst1), "Test('hello', 'world')")

    eq_(test_inst1, test_inst2)
    assert_not_equals(test_inst1, test_inst3)
    assert_not_equals(test_inst1, None)


def test_transposed_view():
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    transposed = TransposedView(grid)

    eq_(grid[0][2], 3)
    eq_(transposed[2][0], 3)
    
    grid[1][2] = 9
    eq_(transposed[2][1], 9)

    transposed[1][2] = 9
    eq_(grid[2][1], 9)
