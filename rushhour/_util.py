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
