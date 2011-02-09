#!/usr/bin/env python
from library import shape, coord

class Buffer (shape.Shape):
    pass

class ViewPort (object):
    """
    A way of viewing 
    """
    _left = 0
    _top = 0
    _width = 0
    _height = 0
    buffer = None
    def __init__ (self, width=10, height=10, buffer=None):
        """
        Create a new viewport object.
        """
        assert buffer.size() >= (width, height)

        self.buffer = buffer

        # Centre the buffer on the screen.
        center = buffer.center()
        self._left = center.x - (width / 2)
        self._top = center.y - (height / 2)
        self._width = width
        self._height = height

    def left (self, count):
        self._left -= count

    def right (self, count):
        self._left += count

    def down (self, count):
        self._top += count

    def up (self, count):
        self._top -= count

    def sect (self):
        start = coord.Coord(self._left, self._top)
        stop = coord.Coord(self._left + self._width, self._top + self._height)
        size = self.buffer.size()

        actual_start = start
        actual_stop = stop

        if start < (0, 0):
            actual_start = coord.Coord(0, 0)
        if stop > size:
            actual_stop = coord.Coord(size)

        sect = self.buffer.section(actual_start, actual_stop)

        sect.pad(self._width, self._height)

        return sect
