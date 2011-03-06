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

class TemplateError (Exception):
    """
    This error is raised whenever there is an issue when creating or formatting
    a template. The error message given specifically explains the actual cause
    of the error, while the trace-back allows locating the error in the source.
    """
    pass

class Template (object):
    """
    Templates are provided to a :class:`TemplateRegion`, and define either
    hard-coded text, a variable, or a combination of some hard-coded text and a
    variable. It also defines how this should be displayed: if the length of
    the template cannot fit within the region, should it be truncated? Not
    displayed? Wrapped onto a new line?
    """

    def __init__ (self, string, name=None, length_handle="truncate", **variables):
        """
        Create a new template.

        :param string: This is the string that is printed to the screen. It
          should contain a series of place-holders (using %(variable)s), whih are
          equivalent to ``variables``.
        :param name: If provided, this is used as the internal representation
          of this template object. *Default None*.
        :param length_handle: How "over-long" lines should be dealt with.
          Options are: "``truncate``", "``wrap``", "``hide``". *Default
          truncate*.
        :param **variables: These keyword arguments should be equivalent to the
          number of place-holders in ``string``.
        """
        assert length_handle in ("truncate", "wrap", "hide")

        self.length_handle = length_handle
        self.string = string
        self.name = name
        self.variables = variables

        for name in variables.keys():
            if hasattr(self, name):
                raise TemplateError("Can't have variable named '%s', it's already an attribute of Template!" % name)

            setattr(self, name, property(lambda self: self.variables[name], lambda self, value: self.variables.__setitem__(name, value)))

    def format (self):
        return self.string % self.variables

    def named (self):
        return self.name is not None

    def __len__ (self):
        return len(self.format())

    def __repr__ (self):
        if self.name is not None:
            return "<Template %s: '%s', %s>" % (self.name, self.string, repr(self.variables))
        else:
            return "<Template '%s', %s>" % (self.string, repr(self.variables))

class TemplateRegion (Region):
    """
    The template defines a way of placing certain strings (either hard-coded or
    variable) on certain parts of a region. For instance, it could be used to
    code up a "heads-up" display. 
    """

    def __init__ (self, start, stop, name, screen, templates):
        """
        This initialises a region according to the provided variables, and then
        initialises a list of templates. These templates can be accessed via
        the :method:`template` function --- which either provides the entire
        list of templates, per-index based access, per-index based replacement,
        or alternately, per-name variations of the above.

        If the templates provide names, then these can be access directly
        through the TemplateRegion object::

            >>> template = Template("%(test)s", name='Test', test=1)
            >>> tr = TemplateRegion(start, stop, name='TestRegion',
            ...   screen=screen, templates=[template])
            >>> tr.Test == template
            True

        :param start: The starting co-ordinate for this region.
        :param stop: The stop co-ordinate for this region.
        :param name: The name used to index this region.
        :param screen: An instance of Screen.
        :param templates: A list of :class:`Template` instances. If these
          templates are named, they will be initialised as members of the
          TemplateRegion.
        """
        super(TemplateRegion, self).__init__(start=start,
        stop=stop, name=name, screen=screen)

        if templates is None:
            templates = []

        self.templates = templates

        if len(self.templates) > self.height():
            raise TemplateError()

        self.indexes = {}

        for index, template in enumerate(self.templates):
            if template.named():
                if hasattr(self, name):
                    raise TemplateError("Template '%s' shadows member '%s'." % (template, template.name))

            self.indexes[name] = index

            setattr(self, name, property(lambda self: self.template(name), lambda self, value: self.template(name, value)))

    def index (self, name):
        """
        Determine the index of a specified template name, or return None.

        :param name: The name of the template, equivalent to
          :method:`Template.name`. If the template is not found, or there are no
          named templates, this operation will always return None.
        """
        if self.indexes.has_key(name):
            return self.indexes[name]

        return None

    def template (self, name=None, value=None):
        """
        Dynamic getter/setter function, which is used both directly as per this
        documentation, and indirectly, as per members of the TemplateRegion
        itself --- each determined by the initialisation function.

        If ``name`` and ``value`` are ``None``, it returns a list of the
        contained templates.

        If ``value`` is ``None``, it returns the template at index ``name``, or
        the template named ``name``.

        Otherwise, it attempts to replace the teplate ``name`` with the
        template ``value``.

        :param name: Either the index of the template, in which case it should
          be an numeric, or the name of the template, in which case it should be
          a string-like object. This value is compared firstly against the
          contained indexes of ``self.templates``, and then against the name
          members of each of the contained templates. *Defalut None*.
        :param value: If provided, this value will replace the template found
          via the above ``name`` parameter.
        """
        if name is None and value is None:
            return self.templates

        if value is None:
            try:
                return self.templates[name]
            except TypeError:
                try:
                    return self.templates[self.index(name)]
                except TypeError:
                    return None

        assert name is not None

        try:
            self.templates[name] = value
        except TypeError:
            try:
                self.templates[self.index(name)] = value
            except TypeError:
                raise TemplateError("Can't find index '%s'!" % name)

        return True

    def as_shape (self, padding=" "):
        """
        This function returns a new :class:`shape.Shape`, its dimensions
        equivalent to the width and height of this region; this shape is
        created by iterating over each of the contained templates and
        formatting them. If a resulting template exceeds the width of the
        region, it is either truncated, wrapped, or hidden according to the
        template's configuration.

        :param padding: For too-short lines, this is the character used to pad
          them. *Default " "*.
        """
        new_shape = shape.Shape(self.width(), self.height(), fill=padding)

        messages = []

        for template in self.templates:
            if len(template) > self.width():
                if template.length_handle == "truncate":
                    messages.append(template.format()[:self.width()])
                elif template.length_handle == "wrap":
                    messages.extend(textwrap.wrap(template.format(), self.width()))
                else:
                    continue

        for y, line in enumerate(messages):
            if len(line) < self.width():
                line += padding * (self.width() - len(line))

            for x, char in enumerate(line):
                new_shape[x][y] = char

        return new_shape

    def blit (self, bshape=None):
        """
        If ``bshape`` is None, this function converts the contained templates
        into a shape and then uses parent functions of this class in order to
        blit it onto the screen.

        If ``bshape`` is not None, it acts exactly like Region.blit.

        :param bshape: The shape to be blitted onto the region. By default,
          this is ``None``, and when it is None,
          :func:`TemplateRegion.as_shape` is called, and ``bshape`` is set
          to this. This is then passed up to parent methods of this class.
          *Default None*.
        """
        if bshape is None:
            bshape = self.as_shape()

        super(TemplateRegion, self).blit(bshape)
