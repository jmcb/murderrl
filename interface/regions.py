#!/usr/bin/env python
"""
Regions are a section of a screen. They are basically a set width and height,
in screen columns and rows, that has been "set aside". The basic
:class:`Region` takes a two co-ordinates: ``start`` and ``stop``. You can then
pass any shape or shape-like object to the Region's :func:`Region.blit`
function.

Extensions of the base Region include :class:`MessageRegion`, whose primary
entry-point is through a list of strings which are outputted to the screen, and
:class:`ViewPortRegion`, whose main purpose is to provide a way of positioning
a ViewPort on the screen.

Finally, there exists :class:`VariableRegion` and variable variations of
:class:`MessageRegion` and :class:`ViewPortRegion`, which allow you to specify
a starting location as well as a percentage of width and screen height the
region should take up.
"""

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
        Create a new region with the following:

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
        Create a new variable region with the following:

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
        """
        This appends a single message string to the current set of messages;
        this will become the "most recent" message, and will be the one
        displayed next time the region is blitted.

        :param message: The next string message.
        """
        self.messages.append(message)

    def as_shape (self, padding=" "):
        """
        Using the information available to the region, this constructs a new
        Shape object which is the width and height of this region. It then uses
        the standard library :mod:`textwrap` module to wrap all recent messages
        that could fit on the screen, then takes these and draws them to the
        shape.

        Finally, the shape is returned. This shape can be used for blitting
        purposes, or it could be used for other purposes.

        :param padding: When short messages are encountered, this value is used
          to "pad" them. Short messages are defined as any message whose length
          is less than the width of the region. *Default " "*.
        """
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

    def blit (self, bshape=None):
        """
        If ``bshape`` is None, this function converts the contained messages
        into a shape and then uses parent functions of this class in order to
        blit it onto the screen.

        If ``bshape`` is not None, it acts exactly like Region.blit.

        :param bshape: The shape to be blitted onto the region. By default,
          this is ``None``, and when it is None,
          :func:`MessageRegion.as_shape` is called, and ``bshape`` is set
          to this. This is then passed up to parent methods of this class.
          *Default None*.
        """
        if bshape is None:
            super(MessageRegion, self).blit(self.as_shape())
        else:
            super(MessageRegion, self).blit(bshape)

class VariableMessageRegion (VariableRegion, MessageRegion):
    """
    This is identical to a normal :class:`MessageRegion`, except that it
    subclasses :class:`VariableRegion` instead of the base :class:`Region`.
    Thus, instead of having a defined height and width passed in by the user by
    defining start and stop co-ordinates, it is instead given a start
    co-ordinate and a series of percentages that describe how much of the
    remaining screen space is to be taken up by this.
    """

    @decorators.extends_multiple(VariableRegion.__init__, MessageRegion.__init__)
    def __init__ (self, *args, **kwargs):
        super(VariableMessageRegion, self).__init__(*args, **kwargs)

class ViewPortRegion (Region):
    """
    This provides a way of placing a ViewPort within a region. It uses the
    values passed to the :class:`Region` to decide how large the resulting
    view-port will be; it also uses a buffer provided to the region to pass
    through to the viewport; finally, it provides accessor functions to both
    the buffer (and for replacing it) and the ViewPort.
    """
    _viewport = None

    @decorators.extends(Region.__init__)
    def __init__ (self, *args, **kwargs):
        super(ViewPortRegion, self).__init__(*args, **kwargs)

        self._viewport = viewport.ViewPort(self.width(), self.height(), buffer=self._buffer)

    def buffer (self, buffer=None):
        """
        Either fetch the buffer contained within our viewport, or replace it.

        :param buffer: If not ``None``, this buffer will replace the buffer
          contained within our viewport. Otherwise, this function will return the
          contained viewport. *Default None*.
        """
        if buffer is None:
            return self._viewport.buffer
        else:
            self._viewport.buffer = buffer
            return self._viewport.buffer

    def viewport (self):
        """
        Returns the viewport object contained within ourselves.
        """
        return self._viewport

    def blit (self, bshape=None):
        """
        If ``bshape`` is None, the result of our contained viewport's `sect`
        method will be blitted onto this region.

        If ``bshape`` is not None, this shape will instead be blitted onto this
        region.

        :param bshape: The shape to be blitted, or ``None``. *Default None*.
        """
        super(ViewPortRegion, self).blit(self.viewport().sect())

class VariableViewPortRegion (VariableRegion, ViewPortRegion):
    """
    As per :class:`VariableMessageRegion`, this class provides a subclass of
    :class:`VariableRegion` for :class:`ViewPortRegion`, allowing you to
    specify a starting location and screen height and width percentages to be
    used. These values will also be used for the creation of the viewport.
    """

    @decorators.extends_multiple(VariableRegion.__init__, ViewPortRegion.__init__)
    def __init__ (self, *args, **kwargs):
        super(VariableViewPortRegion, self).__init__(*args, **kwargs)

class Template (object):
    """
    Templates are provided to a :class:`TemplateRegion`, and define either
    hard-coded text, a variable, or a combination of some hard-coded text and a
    variable. It also defines how this should be displayed: if the length of
    the template cannot fit within the region, should it be truncated? Not
    displayed? Wrapped onto a new line?
    """

    def __init__ (self, string, length_handle="truncate", **variables):
        """
        Create a new template.

        :param string: This is the string that is printed to the screen. It
          should contain a series of place-holders (using %(variable)s), whih are
          equivalent to ``variables``.
        :param length_handle: How "over-long" lines should be dealt with.
          Options are: "``truncate``", "``wrap``", "``hide``". *Default
          truncate*.
        :param **variables: These keyword arguments should be equivalent to the
          number of place-holders in ``string``.
        """
        pass

class TemplateRegion (Region):
    """
    The template defines a way of placing certain strings (either hard-coded or
    variable) on certain parts of a region. For instance, it could be used to
    code up a "heads-up" display. 
    """
    pass
