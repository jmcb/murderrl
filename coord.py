#!/usr/bin/env python

class RectangleIterator (object):
    def __init__ (self, start_point, stop_point=None):
        """
        Iterator over a rectangle of points starting at ``start_point``, finishing
        at ``stop_point``. If ``stop_point`` is undefined, will instead use Coord(0, 0)
        as ``start_point`` and then generate a rectangle Coord(0,0) -> ``start_point``.
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
        else:
            self.x = x
            self.y = y
    def valid (self):
        return (self.x > -1 and self.y > -1)
    def __str__ (self):
        return "%s,%s" % (self.x, self.y)
    def __repr__ (self):
        return "<Coord %s,%s>" % (self.x, self.y)
    def __add__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return Coord(self.x+other.x, self.y+other.y)
    def __iadd__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        self.x += other.x
        self.y += other.y
        return self
    def __sub__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return Coord(self.x-other.x, self.y-other.y)
    def __isub__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        self.x -= other.x
        self.y -= other.y
        return self
    def __mul__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return Coord(self.x*other.x, self.y*other.y)
    def __imul__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        self.x *= other.x
        self.y *= other.y
        return self
    def __div__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return Coord(self.x/other.x, self.y/other.y)
    def __floordiv__(self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return Coord(floor(self.x/other.x), floor(self.y/other.y))
    def __idiv__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        self.x /= other.x
        self.y /= other.y
        return self
    def __ifloordiv__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        self.x = floor(self.x/other.x)
        self.y = floor(self.y/other.y)
        return self
    def __lt__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x<other.x and self.y<other.y)
    def __le__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x<=other.x and self.y<=other.y)
    def __eq__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x==other.x and self.y==other.y)
    def __ne__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x!=other.x and self.y!=other.y)
    def __gt__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x>other.x and self.y>other.y)
    def __ge__ (self, other):
        if isinstance(other, tuple):
            other = Coord(other[0], other[1])
        elif not isinstance(other, Coord):
            other = Coord(other, other)
        return (self.x>=other.x and self.y>=other.y)

