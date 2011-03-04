#!/usr/bin/env python

import textwrap

from library import coord, shape, viewport

class Region (object):
    start = None
    stop = None
    name = None
    def __init__ (self, start, stop, name, screen):
        self.start = start
        self.stop = stop
        self.name = name
        self.screen = screen

    def height (self):
        return self.stop.y - self.start.y

    def width (self):
        return self.stop.x - self.start.x

    def size (self):
        return coord.Size(self.stop - self.start)

    def blit (self, from_shape):
        """
        This function prints of much as `shape` as it can within the bounds
        described by this range. This information is "written" to the screen,
        and is therefore immediately visible. It does not wipe out any colours
        in the area controlled by this image.
        """
        if from_shape.size() > self.size():
            from_shape = from_shape.section(coord.Coord(0, 0), self.size())

        for index, char in from_shape:
            self.screen.glyphs()[index+self.start] = char

class VariableRegion (Region):
    def __init__ (self, per_width, per_height, name, screen, min_width=0, min_height=0):
        sw, sh = screen.size()

        width = max(round(sw*(per_width/100)), min_width)
        height = max(round(sh*(per_height/100)), min_height)

        super(VariableRegion, self).__init__(width, height, name, screen)

class MessageRegion ():
    messages = None

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

