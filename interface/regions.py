#!/usr/bin/env python
"""
Regions are a section of a screen. They are basically a set width and height,
in screen columns and rows, that has been "set aside". The basic
:class:`Region` takes a two co-ordinates: ``start`` and ``stop``. You can then
pass any shape or shape-like object to the Region's :function:`Region.blit`
function.

Extensions of the base Region include :class:`MessageRegion`, whose primary
entry-point is through a list of strings which are outputted to the screen, and
:class:`ViewPortRegion`, whose main purpose is to provide a way of positioning
a ViewPort on the screen.

Finally, there exists :class:`VariableRegion` and variable variations of
:class:`MessageRegion` and :class:`ViewPortRegion`, which allow you to specify
a starting location as well as a percentage of width and screen height the
region should take up.  """

import textwrap

from library import coord, shape, viewport
from util import decorators

class Region (object):
    """
    The basic region from which all other regions are derived.
    """
    start = None
    stop = None
    name = None
    def __init__ (self, start, stop, name, screen):
        """
        :param start: The starting co-ordinate for this region.
        :param stop: The stop co-ordinate for this region.
        :param name: The name used to index this region.
        :param screen: An instance of Screen.
        """
        self.start = start
        self.stop = stop
        self.name = name
        self.screen = screen

    def height (self):
        """
        Returns the height in rows of this region.
        """
        return self.stop.y - self.start.y

    def width (self):
        """
        Returns the width in columns of this region.
        """
        return self.stop.x - self.start.x

    def size (self):
        """
        Returns the size of this region.
        """
        return coord.Size(self.stop - self.start)

    def blit (self, from_shape):
        """
        This function prints of much as `from_shape` as it can within the
        bounds described by this range. This information is "written" to the
        screen, and is therefore immediately visible. It does not wipe out any
        colours in the area controlled by this image.

        :param from_shape: The shape to blit from.
        """
        if from_shape.size() > self.size():
            from_shape = from_shape.section(coord.Coord(0, 0), self.size())

        for index, char in from_shape:
            self.screen.glyphs()[index+self.start] = char

class VariableRegion (Region):
    """
    Instead of defining a start and stop co-ordinate for this Region, you
    instead define a starting co-ordinate and a percentage of remaining screen
    space that it should take up; therefore, the ``stop`` parameter needs to be
    the left-most co-ordinate of the region.
    """
    def __init__ (self, start, per_width, per_height, name, screen, min_width=0, min_height=0):
        """
        :param start: The starting location for this region.
        :param per_width: How big a percentage of columns to take up (out of
          100).
        :param per_height: How big a percentage of rows to take up (out of 100)
        :param name: The name of this region.
        :param screen: The Screen instance of this region.
        :param min_width: The minimum number of columns that should be assigned
          this.
        :param min_height: The minimum number of rows that should be assigned
          to this."""
        sw, sh = screen.size() - start

        width = max(round(sw*(per_width/100)), min_width)
        height = max(round(sh*(per_height/100)), min_height)

        stop = coord.Coord(width, height)

        super(VariableRegion, self).__init__(start, stop, name, screen)

class MessageRegion (Region):
    """
    A message region is a buffer of strings contained within a list. The latest
    strings are displayed at the bottom of the region, with older strings above
    that, until it runs out of space; thus, you will always have the most
    recent message on the screen.
    """
    messages = None

    @decorators.extends(Region.__init__)
    def __init__ (self, *args, **kwargs):
        super(MessageRegion, self).__init__(*args, **kwargs)

        self.messages = []

    def append (self, message):
        self.messages.append(message)

    def as_shape (self, padding=" "):
        new_shape = shape.Shape(self.width(), self.height())

        lines = []
        for line in self.messages[-self.height():]:
            lines.extend(textwrap.wrap(line, self.width()))

        for y, line in enumerate(lines[-self.height():]):
            if len(line) < self.width():
                line += padding * (self.width() - len(line))

            for x, char in enumerate(line):
                new_shape[x][y] = char

        return new_shape

    def blit (self):
        """
        This function writes the contents of messages to the region defined on
        the screen for our use, performing word-wrapping as required.
        """
        super(MessageRegion, self).blit(self.as_shape())

class VariableMessageRegion (VariableRegion, MessageRegion):
    def __init__ (self, *args, **kwargs):
        super(VariableMessageRegion, self).__init__(*args, **kwargs)

class ViewPortRegion (Region):
    _viewport = None
    _buffer = None

    def __init__ (self, *args, **kwargs):
        super(ViewPortRegion, self).__init__(*args, **kwargs)

        self._viewport = viewport.ViewPort(self.width(), self.height(), buffer=self._buffer)

    def buffer (self, buffer=None):
        if buffer is None:
            return self._buffer
        else:
            self._buffer = buffer
            return self.buffer

    def viewport (self):
        return self._viewport

    def blit (self):
        super(ViewPortRegion, self).blit(self.viwer().sect())

class VariableViewPortRegion (VariableRegion, ViewPortRegion):
    def __init__ (self, *args, **kwargs):
        super(VariableViewPortRegion, self).__init__(*args, **kwargs)

