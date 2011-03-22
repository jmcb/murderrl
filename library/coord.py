#!/usr/bin/env python

class CoordError (Exception): pass

class RectangleIterator (object):
    def __init__ (self, start_point, stop_point=None):
        """
        Iterator over a rectangle of points starting at ``start_point``, finishing
        at ``stop_point``.

        :``start_point``: The starting location of rectangle; if ``stop_point``
                          is undefined, ``start_point`` will become ``Coord(0,0)``
                          and the original start point will be used as the stop
                          point. *Required*.
        :``stop_point``: The finishing location of the rectangle. *Default None*.
        """
        if stop_point is None:
            stop_point = start_point
            start_point = Coord(0, 0)
        self.start_point = start_point
        self.stop_point = stop_point

        assert self.stop_point >= self.start_point
    def __iter__ (self):
        for x in xrange(self.start_point.x, self.stop_point.x):
            for y in xrange(self.start_point.y, self.stop_point.y):
                yield Coord(x, y)
    def __repr__ (self):
        return "<RectangleIterator: %s to %s>" % (self.start_point, self.stop_point)

class AdjacencyIterator (RectangleIterator):
    def __init__ (self, center_point, diag_too = False):
        """
        Iterator over the neighbouring points around a given location.

        :``center_point``: The central point. *Required*.
        :``diag_too``: If true, diagonally adjacent points are included. *Default False*.
        """
        if diag_too:
            self.__init__(RectangleIterator, center_point - Coord(1, 1), center_point + Coord(1, 1))
        else:
            self.center_point = center_point

    def __iter__ (self):
        dirs = [DIR_NORTH, DIR_EAST, DIR_SOUTH, DIR_WEST]
        for d in dirs:
            pos = self.center_point + d
            if pos < POS_ORIGIN:
                continue
            yield pos

    def __repr__ (self):
        return "<AdjacencyIterator: %s>" % (self.pos)

class Coord (object):
    """
    Simple representation of a co-ordinate. 0,0 is assumed to be the top-left
    base co-ordinate. A co-ordinate defined as -1,-1 is assumed to be invalid.
    However, negative co-ordinates may be useful for co-ordinate arithmetic.
    """
    x = -1
    y = -1
    def __init__ (self, x=-1, y=-1):
        if isinstance(x, tuple):
            self.x, self.y = x
        elif isinstance(x, Coord):
            self.x, self.y = x.as_tuple()
        else:
            self.x = x
            self.y = y
    def valid (self):
        return (self.x > -1 and self.y > -1)
    def as_tuple (self):
        return (self.x, self.y)
    def __str__ (self):
        return "%s,%s" % (self.x, self.y)
    def __repr__ (self):
        return "<Coord %s,%s>" % (self.x, self.y)
    def __add__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return self.__class__(self.x+other.x, self.y+other.y)
    def __iadd__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        self.x += other.x
        self.y += other.y
        return self
    def __sub__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return self.__class__(self.x-other.x, self.y-other.y)
    def __isub__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        self.x -= other.x
        self.y -= other.y
        return self
    def __mul__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return self.__class__(self.x*other.x, self.y*other.y)
    def __imul__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        self.x *= other.x
        self.y *= other.y
        return self
    def __div__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return self.__class__(self.x/other.x, self.y/other.y)
    def __floordiv__(self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return self.__class__(floor(self.x/other.x), floor(self.y/other.y))
    def __idiv__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        self.x /= other.x
        self.y /= other.y
        return self
    def __ifloordiv__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        self.x = floor(self.x/other.x)
        self.y = floor(self.y/other.y)
        return self
    def __lt__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x<other.x or self.y<other.y)
    def __le__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x<=other.x or self.y<=other.y)
    def __eq__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x==other.x and self.y==other.y)
    def __ne__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x!=other.x or self.y!=other.y)
    def __gt__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x>other.x or self.y>other.y)
    def __ge__ (self, other):
        if isinstance(other, tuple):
            other = self.__class__(other[0], other[1])
        elif not isinstance(other, self.__class__):
            other = self.__class__(other, other)
        return (self.x>=other.x or self.y>=other.y)
    def __iter__ (self):
        yield self.x
        yield self.y

class Size (Coord):
    """
    A specific representation of size using width and height.
    """
    width = property(lambda self: self.x, lambda self, width: self.__setattr__("x", width))
    height = property(lambda self: self.y, lambda self, width: self.__setattr__("y", width))
    def __init__ (self, width=-1, height=-1):
        if isinstance(width, tuple):
            height = width[1]
            width = width[0]
        elif isinstance(width, Coord):
            width, height = width.as_tuple()
        elif not isinstance(width, int):
            raise CoordError, "Can't use '%s' as a width." % width
        Coord.__init__(self, width, height)
    def __repr__ (self):
        return "<Size width=%s height=%s>" % (self.width, self.height)

class AutoDimension (int):
    """
    An automatically sized integer. As a string, it is represented by infinity.
    It is always larger than other integers, never less than nor equal to.
    """
    def __lt__ (self, other):
        return False
    def __le__ (self, other):
        return False
    def __eq__ (self, other):
        return False
    def __ne__ (self, other):
        return True
    def __gt__ (self, other):
        return True
    def __ge__ (self, other):
        return True
    def __repr__ (self):
        return str(self)
    def __str__ (self):
        return u"\u221e".encode("utf-8")
    __add__ = property(lambda self, other: self)
    __iadd__ = property(lambda self, other: self)
    __sub__ = property(lambda self, other: self)
    __isub__ = property(lambda self, other: self)
    __mul__ = property(lambda self, other: self)
    __imul__ = property(lambda self, other: self)
    __div__ = property(lambda self, other: self)
    __floordiv__ = property(lambda self, other: self)
    __idiv__ = property(lambda self, other: self)
    __ifloordiv__ = property(lambda self, other: self)

class AutoSize (Size):
    """
    An automatic size. For comparative purposes, it is always larger than
    something else--never equal and never smaller.
    """
    def __init__ (self):
        Size.__init__(self, AutoDimension(), AutoDimension())
    def valid (self):
        return True
    def __repr__ (self):
        return "<AutoSize width=%s,height=%s>" % (self.width, self.height)
    def __lt__ (self, other):
        return False
    def __le__ (self, other):
        return False
    def __eq__ (self, other):
        return False
    def __ne__ (self, other):
        return True
    def __gt__ (self, other):
        return True
    def __ge__ (self, other):
        return True

    # These functions are stubbed out, as an automatic size cannot be
    # manipulated, but always returns itself.
    __add__ = property(lambda self, other: self)
    __iadd__ = property(lambda self, other: self)
    __sub__ = property(lambda self, other: self)
    __isub__ = property(lambda self, other: self)
    __mul__ = property(lambda self, other: self)
    __imul__ = property(lambda self, other: self)
    __div__ = property(lambda self, other: self)
    __floordiv__ = property(lambda self, other: self)
    __idiv__ = property(lambda self, other: self)
    __ifloordiv__ = property(lambda self, other: self)

# Define directions.
DIR_NORTH   = Coord(0, -1)
DIR_SOUTH   = Coord(0, +1)
DIR_WEST    = Coord(-1, 0)
DIR_EAST    = Coord(+1, 0)
DIR_NOWHERE = Coord(0, 0)
# for convenience, this time meaning the top left corner of screen or shape
POS_ORIGIN  = Coord(0, 0)
