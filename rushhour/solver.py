from collections import deque


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
    def __getattr__(self, name):
        return getattr(self._board, name)
    def move(self, car, direction, count):
        clone = self._board.copy()
        clone.move(car, direction, count)
        return ImmutableBoard(clone)


def solve(board):
    # Make an immutable copy.
    board = ImmutableBoard(board)
    if board.is_victory():
        return []

    seen = set(board.get_state())
    stack = deque([(board, ())])

    while stack:
        state, path = stack.popleft()
        for move in state.get_moves():
            new_state = state.move(*move)
            new_path = path + (move,)
            if new_state.is_victory():
                return list(new_path)

            frozen = new_state.get_state()
            if frozen in seen:
                continue
            seen.add(frozen)
            stack.append((new_state, new_path))
