class SlottedDefaults(object):
    """Provides default implementation for some methods based on slots."""
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        for slot in self.__slots__:
            if getattr(self, slot) != getattr(other, slot):
                return False
        return True

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ', '.join(
            repr(getattr(self, slot)) for slot in self.__slots__
        ))

    def __hash__(self):
        return hash(tuple(getattr(self, slot) for slot in self.__slots__))

class TransposedView(object):
    """Represents a transposed view of a list of lists."""

    class _Column(object):
        def __init__(self, grid, idx):
            self._grid = grid
            self._idx = idx

        def __getitem__(self, idx):
            return self._grid[idx][self._idx]

        def __setitem__(self, idx, val):
            self._grid[idx][self._idx] = val

    def __init__(self, grid):
        self._grid = grid

    def __getitem__(self, idx):
        return self._Column(self._grid, idx)
