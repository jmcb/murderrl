#!/usr/bin/env python

import shape, coord
from collections import namedtuple
import copy

class CollectionCoord (coord.Coord):
    """
    A Coord that references a specific ShapeCollection.

    This allows for iteration over areas of a ShapeCollection and also directly
    accessing them.
    """
    def __init__ (self, collection, c):
        """
        Create a new CollectionCoord.

        :``collection``: Which collection this references.
        :``coord``: The coordinates of that Collection.
        """
        self.collection = collection
        coord.Coord.__init__(self, c)

    def get (self):
        """
        Fetch the glyphs contained with these points, otherwise return None.
        """
        result = self.collection[self]
        if result == []:
            return None
        else:
            return result

    def set (self, value):
        """
        Set the glyph connected with this Coord to ``value``.

        :``value``: The value to set. See ``ShapeCollection:__setitem__``.
        """
        self.collection[self] = value

    def __str__ (self):
        return str(self.get())

    def __repr__ (self):
        return "<CollectionCoord %s,%s: %s>" % (self.x, self.y, self.get())

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
        Wrapper over self.shape.width.
        """
        return self.shape.width()
    def height (self):
        """
        Wrapper over self.shape.height.
        """
        return self.shape.height()
    def pos (self):
        return self.coord
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
                    if isinstance(s, shape.Shape):
                        s = ShapeCoord(s, coord.Coord(0, 0))
                    elif isinstance(s, tuple) or isinstance(s, list) and len(s) == 2:
                        s = ShapeCoord(s[0], s[1])
                    else:
                        assert isinstance(s, ShapeCoord)
                self._shapes.append(s)

    def combine (self):
        """
        Converts a collection into a single Shape by drawing all ShapeCoords
        onto an automatically shaped canvas.

        Doesn't currently provide error checking. Should.
        """
        # We take the largest and work on that, ignoring its coord.

        base = shape.AutoShape()

        for sc in self._shapes:
            base.draw_on(sc.shape, sc.coord, False)

        return base.as_shape()

    def sort (self):
        """
        In-place sorting by size!
        """
        self._shapes.sort(cmp=lambda a, b: cmp(b.shape.size(), a.shape.size()))

    def append (self, item, c=None):
        """
        As with the initialisation function, all Shapes passed in are here
        converted into ShapeCoords, using Coord(0, 0) as their offset. All other
        instances are not allowed.
        """
        if isinstance(item, ShapeCoord):
            self._shapes.append(item)
        else:
            if c is not None:
                item = ShapeCoord(item, c)
            elif isinstance(item, shape.Shape):
                item = ShapeCoord(item, coord.Coord(0, 0))

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
        size = coord.Size()

        for shape in self._shapes:
            shape, c = shape
            if shape.width() + c.x > size.width:
                size.width = shape.width() + c.x
            if shape.height() + c.y > size.height:
                size.height = shape.height() + c.y

        return size

    def copy (self):
        """
        Returns a copy of this collection.
        """
        return ShapeCollection(copy.copy(self._shapes))

    def column (self, column):
        """
        Provides an iteration of CollectionCoords.

        :``column``: Which column you want to iterate over.
        """
        assert column <= self.width()
        for y in xrange(self.height()):
            yield CollectionCoord(self, coord.Coord(column, y))

    def row (self, row):
        """
        Provides an iteration of CollectionCoords.

        :``row``: Which row you want to iterate over.
        """
        assert row <= self.height()
        for x in xrange(self.width()):
            yield CollectionCoord(self, coord.Coord(x, row))

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
            if sc.coord < coord.Coord(0, 0):
                raise shape.ShapeError, "Shape indexed %s already had a negative offset!" % index
            if sc.coord+offset < coord.Coord(0, 0):
                raise shape.ShapeError, "Adding %s to %s results in %s! Cannot perform negative offsetting." % (offset, sc.coord, sc.coord+offset)

            new_self.append(ShapeCoord(sc.shape, coord.Coord(sc.coord + offset)))

        self._shapes = new_self

    def insert (self, index, item):
        """
        Insert ``item`` at ``index``, shifting contents down by one. If the
        index is beyond the bounds of the collection, it will be appended
        instead.

        Returns the index that the item was actually inserted at.

        :``index``: What index to insert the item at.
        :``item``: The shape to insert.
        """
        if not isinstance(item, ShapeCoord):
            item = ShapeCoord(item, coord.Coord(0, 0))

        assert isinstance(item, ShapeCoord)

        if len(self) <= index:
            self._shapes.append(item)
            return len(self) - 1

        self._shapes.insert(index, item)
        return index

    def __getitem__ (self, item):
        """
        If ``item`` is an integer:

        Fetch item index ``item`` from the collection of ShapeCoords.

        If ``item`` is a Coord instance:

        Attempt to locate ``item`` in the contained ShapeCoords. If ``item`` is
        contained within multiple shapes, a list of them will be returned.

        :``item``: The item to be fetched. Either an integer or a Coord.
        """
        if isinstance(item, int):
            return self._shapes.__getitem__(item)
        else:
            results = []
            for sc in self._shapes:
                try:
                    results.append(sc.shape[item-sc.coord])
                except:
                    pass
            results = list(set(results))
            if len(results) == 1:
                return results[0]
            else:
                return results

    def __setitem__ (self, item, value):
        """
        If ``item`` is an integer:

        Insert ``value`` at ``item``, replacing whatever ShapeCoord is existent
        there.

        :``item``: The index the value is to be inserted at.
        :``value``: The value to be inserted. This is automatically cased
                    from a Shape into a ShapeCoord(Shape, Coord(0, 0)).
                    Otherwise it is assumed to be a ShapeCoord. All other
                    types will cause an error.

        If ``item`` is an instance of Coord:

        Insert ``value`` at ``item`` in each Shape contained within. If ``item``
        is found in multiple shapes, it will set ``value`` in each one; if
        ``value`` is iterable and multiple instances are found, values will be
        applied from ``value[0]`` onwards. If it runs out of values in
        ``value``, it will cease setting and return.

        :``item``: Instance of Coord.
        :``value``: Either one of or a list of width one strings.
        """
        if isinstance(item, int):
            if isinstance(value, shape.Shape):
                value = ShapeCoord(shape, coord.Coord(0, 0))
            assert isinstance(value, ShapeCoord)
            result = self._shapes.__setitem__(item, value)
            return result
        else:
            if not isinstance(value, list):
                value = [value] * len(self)

            for sc in self._shapes:
                if len(value) == 0:
                    return

                tval = value.pop(0)

                if item - sc.coord < (0, 0):
                    continue

                try:
                    sc.shape[item-sc.coord] = tval;
                except Exception:
                    pass

    def reverse (self):
        """
        Performs an in-place reversing of the contents of this ShapeCollection.
        This has the effect of reversing the priority: items added earlier will
        be drawn later, and vice versa. For example::

          >> coll = ShapeCollection()
          >> coll.append(Shape(3, 3, "Y"))
          >> coll.append(Shape(3, 3, "X"))

        Combining this will result in::

          >> print coll.combine()
          XXX
          XXX
          XXX

        Calling reverse before combining results in:

          >> coll.reverse()
          >> print coll.combine()
          YYY
          YYY
          YYY
        """
        self._shapes.reverse()

    def reversed (self):
        """
        Returns a copy of this collection that has been reversed. See
        ``ShapeCollection::reverse``.
        """
        copy = self.copy()
        copy.reverse()
        return copy

    def draw_on (self, target_shape, offset=None):
        """
        Via direct canvas access, draws the contents of ``shape`` onto the
        relevant spots of each canvas contained within.

        :``target``: The shape that should be drawn on this collection. If
                     the shape is larger than the contained shapes, only
                     the section that can be contained within the contained
                     shapes will be drawn.
        :``offset``: A Coord denoting by how much the shape should be offset
                     before drawing. *Default None*.
        """
        assert isinstance(target_shape, shape.Shape)

        for point, glyph in target_shape:
            if offset is not None:
                point += offset
            self[point] = glyph

    def place_on (self, new_collection, offset=None):
        """
        Offset the contents of ``new_collection`` by ``offset`` and then extend
        this collection with the contents of ``new_collection``.

        ``new_collection``: An instance of ShapeCollection, or one of its
                            subclasses.
        ``offset``: A Coord denoting by how much the ``new_collection`` should
                    be offset. *Default None*.
        """
        if offset:
            new_collection.offset(offset)
        self.extend(new_collection)

    def prioritise (self, index, priority=True):
        """
        Alter the priority of ``index``. Priority basically equates to the
        location within the ShapeCollection: indexes with a higher priority are
        drawn later and are thus less likely to be overriden by another shape;
        likewise, indexes with lower priorities are drawn earlier and a thus
        more likely to be override by another shape.

        Priorities are only as valid as long as new items are not added to the
        collection.

        Returns the new index of the item.

        :``index``: The index you wish to prioritise.
        :``priority``: The priority you want to set the index to. Negative
                       numbers will decrease the priority, and positive numbers
                       increase it. If True, the priority will be increased to
                       as high as possible. If False, it will be decreased to as
                       low as possible. *Default True*.
        """
        assert isinstance(index, int)

        if index < 0:
            index = len(self) + index

        assert index < len(self)

        if priority is True:
            item = self.pop(index)
            self.append(item)
            return len(self)-1
        elif priority is False:
            item = self.pop(index)
            self.insert(0, item)
            return 0

        assert isinstance(priority, int)

        if priority < 0:
            new_priority = len(self) + priority
        else:
            new_priority = index + priority

        assert new_priority >= 0
        item = self.pop(index)
        self.insert(new_priority, item)

        if new_priority >= len(self):
            return len(self) - 1

        return new_priority

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

