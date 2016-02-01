from nose.tools import eq_, ok_
import pickle

from rushhour.board import board_from_string, Car, Direction
from rushhour.solver import solve


def _check_solves(board, moves):
    board_copy = pickle.loads(pickle.dumps(board))
    for move in moves:
        board_copy.move(*move)
    return board_copy.is_victory()


def test_solve_simple_case():
    board = board_from_string("""\
......
......
rr....
......
......
......
""")

    eq_(solve(board), [
        (Car('r', Direction.horizontal, 2), Direction.horizontal, 4),
    ])


def test_solve_solves_solved_board():
    board = board_from_string("""\
......
......
....rr
......
......
......
""")

    eq_(solve(board), [
    ])


def test_first_level():
    board = board_from_string("""\
.....A
.....A
.rr..A
......
......
......
""")
    moves = solve(board)

    ok_(_check_solves(board, moves))
    eq_(moves, [
        (Car('A', Direction.vertical, 3), Direction.vertical, 3),
        (Car('r', Direction.horizontal, 2), Direction.horizontal, 3),
    ])


def test_complex_test_case():
    board = board_from_string("""\
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
""")

    moves = solve(board)
    for move in moves:
        board.move(*move)
    ok_(board.is_victory())
    eq_(len(moves), 13)


def test_solve_many_boards():
    def _check(lvl, board_desc, num_moves):
        board = board_from_string(board_desc)
        moves = solve(board)
        ok_(_check_solves(board, moves))
        eq_(len(moves), num_moves)

    cases = [
        ("lvl01", "AA...B\nC..D.B\nCrrD.B\nC..D..\nE...FF\nE.GGG.\n",  8),
        ("lvl10", "AAB.CC\nDDB..E\nFrr..E\nFGGG.E\nF..HII\nJJ.HKK\n", 17),
        ("lvl11", "ABBC..\nA..C..\nArrC..\n..DEEE\n..D..F\n..GGGF\n", 25),
        ("lvl20", "A..BBB\nACCD..\nrrED.F\n..E..F\n..GHHF\n..GIII\n", 10),
        ("lvl21", "AABC..\nD.BC..\nDrrC..\nDEEE..\n......\n...FFF\n", 21),
        ("lvl25", "AAB.CC\nDDB..E\nFrr.GE\nFHHHGE\nFI.JKK\n.I.JLL\n", 27),
        ("lvl30", "A.BCCC\nA.BD..\nArrD..\nEEFF.G\n.....G\nHHII.G\n", 32),
        ("lvl31", "AA.BBB\n...CDD\nErrC.F\nE.GHHF\nIIG..F\n..GKKK\n", 37),
        ("lvl40", "ABB.C.\nADE.CF\nADErrF\nGGGH.F\n..IHJJ\nKKILL.\n", 51),
    ]

    for lvl, board_desc, num_moves in cases:
        yield _check, lvl, board_desc, num_moves


def test_hardest_board():
    # According to http://www.ulb.ac.be/di/algo/secollet/papers/crs06.pdf,
    # this is actually the hardest composition.
    # It is supposed to take 93 steps, but the solver solves it in 49. This is
    # due to a counting-difference in how slides across multiple squares is
    # counted (red car, 4 to the left can be counted as either 1 or 4 steps).
    board = board_from_string("""\
AAABCD
EFFBCD
E.rrCD
HHI...
.JI.KK
.JLLMM
""")

    moves = solve(board)
    ok_(_check_solves(board, moves))
    eq_(len(moves), 49)
