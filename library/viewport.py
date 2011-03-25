#!/usr/bin/env python
from library import coord

class ViewPort (object):
    """
    A way of viewing 
    """
    _left   = 0
    _top    = 0
    _width  = 0
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
        self._left   = 0 #(center.x - width) / 2
        self._top    = 0 #(center.y - height) / 2
        self._width  = width
        self._height = height

    def left (self, count):
        self._left -= count

    def right (self, count):
        self._left += count

    def down (self, count):
        self._top += count

    def up (self, count):
        self._top -= count

    def size (self):
        return coord.Coord(self._width, self._height)

    def centre (self, pos, stop):
        # Centre the buffer on the screen.
        self._left = max(0, pos.x - self._width/2)
        self._top  = max(0, pos.y - self._height/2)
        if self._left + self._width > stop.x:
            self._left = stop.x - self._width
        if self._top + self._height > stop.y:
            self._top = stop.y - self._height

    def sect (self):
        width  = self._width
        height = self._height

        left_padding = False
        top_padding  = False

        left = self._left
        top  = self._top

        start = coord.Coord(left, top)
        stop  = coord.Coord(left + width, top + height)

        bwidth, bheight = self.buffer.size()

        if start.x < 0:
            left_padding = True
            start.x = 0
        if start.y < 0:
            top_padding = True
            start.y = 0
        if stop.x > bwidth:
            stop.x = bwidth
        if stop.y > bheight:
            stop.y = bheight

        sect = self.buffer.section(start, stop)

        if sect.width() < width:
            if left_padding:
                sect.pad(num_cols=width)
            else:
                sect.normalise(width=width)
        if sect.height() < height:
            if top_padding:
                sect.pad(num_rows=height)
            else:
                sect.normalise(height=height)

        return sect

    def pos_in_section (self, pos):
        if (pos.x <= self._left or pos.x >= self._left + self._width
        or pos.y <= self._top or pos.y >= self._top + self._height):
            return False
        return True
