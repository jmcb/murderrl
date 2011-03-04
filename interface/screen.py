#!/usr/bin/env python
"""
The "screen" is the rawest part of the interface. It consists entirely of a
grid of characters, equivalent to the width and height of the current display.
"""

import textwrap

from library import shape, coord, viewport

class Grid (object):
    _grid = None
    def __init__ (self, width=0, height=0):
        self._grid = []

        for row in xrange(height):
            row = []
            for column in xrange(width):
                row.append(None)
            self._grid.append(row)

    def at (self, c, x=None):
        if x is not None:
            c = coord.Coord(coord, x)

        try:
            return self._grid[c.y][c.x]
        except IndexError:
            return None

    def set (self, c, x=None, grid=None):
        if x is not None:
            c = coord.Coord(c, x)
        else:
            grid = x

        try:
            self._grid[c.y][c.x] = grid
        except IndexError:
            return False

        return True

class ScreenGrid (shape.Shape):
    pass

class ColourGrid (Grid):
    pass

class Screen (object):
    _regions = None
    _glyphs = None
    _colours = None
    _screen = None

    def __init__ (self, size, phys_screen):
        width, height = size

        self._glyphs = ScreenGrid(width=width, height=height, fill=" ")
        self._colours = ColourGrid(width=width, height=height)

        self._regions = []

        self._screen = phys_screen

    def region (self, start, stop=None, name=None):
        if stop is not None:
            new_region = Region(start, stop, name)
        else:
            new_region = start
            name = stop

        self._regions.append(new_region)

    def regions (self, index=None):
        if index is not None:
            try:
                return self._regions[index]
            except TypeError:
                return self.region_by_name(index)
        else:
            return self._regions[:]

    def region_by_name (self, name):
        for region in self.regions():
            if region.name == name:
                return region

        return None

    def colours (self):
        return self._colours

    def glyphs (self):
        return self._glyphs

    def physical (self):
        return self._screen

    def blit (self):
        """
        This blits the entire contents of self.glyphs onto the screen -- using
        colours where appropriate.
        """

        for c, glyph in self.glyphs():
            colour = self.colours().at(c)

            self.physical().put(glyph, c, colour)
