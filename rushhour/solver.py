from collections import deque
import pickle


# Solver design.
#
# Perform a breadth-first search through the search-space. To make it a bit
# problem-agnostic, we require that there are several things supplied:
#
# - Initial state : GameState
# - Victory checker : GameState -> Bool (Very important)
# - Move lister : GameState -> GameMove
# - Move applier : GameState -> GameMove -> GameState
#
# Here it is assumed that all is acting on immutable objects, because that
# makes the code simpler.
class ImmutableBoard(object):
    def __init__(self, board):
        self._board = board
    def get_moves(self):
        return self._board.get_moves()
    def __str__(self):
        return str(self._board)
    def car_at_position(self, pos_x, pos_y):
        return self._board.car_at_position(pos_x, pos_y)
    def is_victory(self):
        return self._board.is_victory()
    def move(self, car, direction, count):
        # This is overkill, we do not need to clone everything, just the
        # important parts.
        clone = pickle.loads(pickle.dumps(self._board))
        clone.move(car, direction, count)
        return ImmutableBoard(clone)


def solve(board):
    # Make an immutable copy.
    board = ImmutableBoard(board)
    if board.is_victory():
        return []

    freeze = str  # Get an immutable description of state.

    seen = set(freeze(board))
    stack = deque([(board, ())])

    while stack:
        state, path = stack.popleft()
        for move in state.get_moves():
            new_state = state.move(*move)
            new_path = path + (move,)
            if new_state.is_victory():
                return list(new_path)

            frozen = freeze(new_state)
            if frozen in seen:
                continue
            seen.add(frozen)
            stack.append((new_state, new_path))
