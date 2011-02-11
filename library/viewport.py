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

        center = self.buffer.center()

        # Centre the buffer on the screen.
        self._left = (center.x - width) / 2
        self._top = (center.y - height) / 2
        self._width = width
        self._height = height

    def left (self, count):
        self._left = max(self._left - count, 0)

    def right (self, count):
        self._left = max(self._left + count, 0)

    def down (self, count):
        self._top = max(self._top + count, 0)

    def up (self, count):
        self._top = max(self._top - count, 0)

    def sect (self):

        left_padding = min(0, self._left)
        top_padding = min(0, self._top)

        left = max(self._left, 0)
        top = max(self._top, 0)

        width = self._width
        height = self._height

        start = coord.Coord(left, top)
        stop = coord.Coord(left + width, top + height)

        bwidth, bheight = self.buffer.size()

        if start < (0, 0):
            start = coord.Coord(0, 0)
        if stop.x > bwidth:
            stop.x = bwidth
        if stop.y > bheight:
            stop.y = bheight

        sect = self.buffer.section(start, stop)

        if left_padding != 0:
            sect.pad(num_cols=-width)
        elif sect.width() < width:
            sect.normalise(width=width)

        if top_padding != 0:
            sect.pad(num_rows=-height)
        elif sect.height() < height:
            sect.normalise(height=height)

        return sect
