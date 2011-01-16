#!/usr/bin/env python
from library.shape import *
from library.coord import *

class ShapeCoord (namedtuple("ShapeCoord", "shape coord")):
    """
    A named tuple pair providing ``shape`` and ``coord`` members. This is primarily
    used by the ShapeCollection class.
    """
    def size (self):
        """
        Wrapper over self.shape.size.
        """
        return self.shape.size()
    def width (self):
        """
        Wraper over self.shape.width.
        """
        return self.shape.width()
    def height (self):
        """
        Wrapper over self.shape.height.
        """
        return self.shape.height()
    def __getattribute__ (self, attr):
        if attr == "shape":
            return tuple.__getitem__(self, 0)
        elif attr == "coord":
            return tuple.__getitem__(self, 1)
        if hasattr(self.shape, attr):
            return self.shape.__getattribute__(attr)
        else:
            return tuple.__getattribute__(self, attr)

class ShapeCollection (object):
    """
    A sortable collection of Shapes and co-ordinates. Can be initiliased from a list
    of ShapeCoords or Shapes. For the latter, these will be wrapped in a ShapeCoord
    using Coord(0, 0) as their co-ordinate.

    You can also ``append`` items, ``pop`` items, assign using ShapeCollection[index]
    notation, and fetch via ShapeCollcetion[index] notation.
    """
    _shapes = None
    def __init__ (self, shapes=None):
        self._shapes = []

        if shapes is not None:
            for s in shapes:
                if not isinstance(s, ShapeCoord):
                    if isinstance(s, Shape):
                        s = ShapeCoord(s, Coord(0, 0))
                    elif isinstance(s, tuple) or isinstance(s, list) and len(s) == 2:
                        s = ShapeCoord(s[0], s[1])
                    else:
                        assert isinstance(s, ShapeCoord)
                self._shapes.append(s)

    def combine (self):
        """
        Converts a collection into a single Shape by taking drawing all ShapeCoords
        onto an automatically shaped canvas.

        Doesn't currently provide error checking. Should.
        """
        # We take the largest and work on that, ignoring its coord.

        base = AutoShape()

        for sc in self._shapes:
            base.draw_on(sc.shape, sc.coord, False)

        return base.as_shape()

    def sort (self):
        """
        In-place sorting by size!
        """
        self._shapes.sort(cmp=lambda a, b: cmp(b.shape.size(), a.shape.size()))

    def append (self, item, coord=None):
        """
        As with the initialisation function, all Shapes passed in are here
        converted into ShapeCoords, using Coord(0, 0) as their offset. All other
        instances are not allowed.
        """
        if isinstance(item, ShapeCoord):
            self._shapes.append(item)
        else:
            if coord is not None:
                item = ShapeCoord(item, coord)
            elif isinstance(item, Shape):
                item = ShapeCoord(item, Coord(0, 0))
            else:
                assert isinstance(item, ShapeCoord)
            self._shapes.append(item)

    def extend (self, items):
        """
        Extends the current collection of ShapeCoords by the passed list of
        items.

        :``items``: An instance of ShapeCollection. *Required*.
        """
        assert isinstance(items, ShapeCollection)
        self._shapes.extend(items)

    def pop (self, index=-1):
        """
        Pop index ``index`` item from the collection of ShapeCoords.

        :``index``: The index in question. *Default -1*.
        """
        item = self._shapes.pop(index)
        return item

    def width (self):
        """
        Returns the width required to contain each member.
        """
        return self.size().width

    def height (self):
        """
        Returns the height required to contain each member.
        """
        return self.size().height

    def size (self):
        """
        Returns the size required to contain each member.
        """
        size = Size()

        for shape in self:
            shape, coord = shape
            if shape.width() + coord.x > size.width:
                size.width = shape.width() + coord.x
            if shape.height() + coord.y > size.height:
                size.height = shape.height() + coord.y

        return size

    def copy (self):
        """
        Returns a copy of this collection.
        """
        return ShapeCollection(self._shapes[:])

    def offset (self, offset):
        """
        Offsets each member of the ShapeCollection by the passed offset.

        :``offset``: A Coord or Size with which to offset each Shape. If this is
                     a negative value, the offsetting will be subtractive;
                     however, if this results in any ShapeCoord being negatively
                     offset, an error will be raised, and the offsetting will be
                     abandoned. *Required*.
        """
        new_self = []

        for index, sc in enumerate(self):
            if sc.coord < Coord(0, 0):
                raise ShapeError, "Shape indexed %s already had a negative offset!" % index
            if sc.coord+offset < Coord(0, 0):
                raise ShapeError, "Adding %s to %s results in %s! Cannot perform negative offsetting." % (offset, sc.coord, sc.coorrd+offset)

            new_self.append(ShapeCoord(sc.shape, Coord(sc.coord + offset)))

        self._shapes = new_self

    def __getitem__ (self, item):
        """
        Fetch item index ``item`` from the collection of ShapeCoords.

        :``item``: The item to be fetched.
        """
        return self._shapes.__getitem__(item)

    def __setitem__ (self, item, value):
        """
        Insert ``value`` at ``item``, replacing whatever ShapeCoord is existent
        there.

        :``item``: The index the value is to be inserted at.
        :``value``: The value to be inserted. This is automatically cased
                    from a Shape into a ShapeCoord(Shape, Coord(0, 0)).
                    Otherwise it is assumed to be a ShapeCoord. All other
                    types will cause an error.
        """
        if isinstance(value, Shape):
            value = ShapeCoord(shape, Coord(0, 0))
        assert isinstance(value, ShapeCoord)
        result = self._shapes.__setitem__(item, value)
        return result

    def __iter__ (self):
        """
        Creates an iterator for the ShapeCoords contained within.
        """
        return iter(self._shapes)

    def __len__ (self):
        """
        Returns the number of ShapeCoords contained within.
        """
        return len(self._shapes)

