import sys

from rushhour.board import board_from_string, Direction
from rushhour.solver import solve


def _sign(v):
    return v / abs(v)


if __name__ == "__main__":
    # Read the board
    if len(sys.argv) == 1:
        board_description = sys.stdin.read()
    else:
        with open(sys.argv[1]) as fp:
            board_description = fp.read()

    # Solve the board
    board = board_from_string(board_description)
    moves = solve(board)

    if moves is None:
        print("Board is not solvable. Sorry.")
    else:
        # Render the board
        for move in moves:
            direction_string = {
                (Direction.horizontal, 1): 'R',
                (Direction.horizontal, -1): 'L',
                (Direction.vertical, 1): 'D',
                (Direction.vertical, -1): 'U',
            }[move[1], _sign(move[2])]
            print("{}{}{}".format(
                move[0].color,
                direction_string,
                abs(move[2]),
            ))
