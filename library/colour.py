#!/usr/bin/env python

class BaseColour (object):
    """
    An agnostic representation of a basic, single-state colour, as used by
    Urwid.
    """
    _colour = None
    _colour_id = None
    def __init__ (self, colour_name, colour_id):
        """
        Create a new colour.

        :``colour_name``: The representation of the colour.
        :``colour_id``: The specific identifier for this colour.
        """
        self._colour = colour_name
        self._colour_id = colour_id

    def is_base (self):
        """
        Determines if this colour is a "base colour", that is, one of the
        "allowed" colours that are defined for use on the console. Currently,
        only these colours are supported, so this is always true.
        """
        return True

    def lighten (self):
        """
        Performs an in-place lightening of the current colour. This function can
        only be currently applied to colours that return True for ``is_base()``.
        """
        if self._colour_id > 8:
            return

        if self._colour == "brown":
            self._colour = "yellow"
            self._colour_id = Colours.YELLOW._colour_id
        elif self._colour == "lightgray":
            self._colour = "white"
            self._colour_id = Colours.WHITE._colour_id
        elif self._colour == "darkgray":
            self._colour = "lightgray"
            self._colour_id = Colours.LIGHTGRAY._colour_id
        elif self._colour == "black":
            self._colour = "darkgray"
            self._colour_id = Colours.DARKGRAY._colour_id
        else:
            self._colour = "light" + self._colour
            self._colour_id += 8

    def lightened (self):
        """
        Return a copy of the current colour that has been lightened.
        """
        c = self.copy()
        c.lighten()
        return c

    def darken (self):
        """
        Perform an in-place darkening of the current colour. This function can
        only be applied to colours that return True for ``is_base()``.
        """
        if self._colour_id < 8 or self._colour_id > 16:
            return

        if self._colour == "yellow":
            self._colour = "brown"
            self._colour_id = Colours.BROWN._colour_id
        elif self._colour == "white":
            self._colour = "lightgray"
            self._colour_id = Colours.LIGHTGRAY._colour_id
        elif self._colour == "lightgray":
            self._colour = "darkgray"
            self._colour_id = Colours.DARKGRAY._colour_id
        elif self._colour == "darkgray":
            self._colour = "black"
            self._colour_id = Colours.BLACK._colour_id
        else:
            self._colour = self._colour.replace("light", "")
            self._colour_id -= 8

    def darkened (self):
        """
        Return a copy of the current colour which has been darkened.
        """
        c = self.copy()
        c.darken()
        return c

    def copy (self):
        """
        Return a copy of the current colour.
        """
        c = BaseColour(self._colour, self._colour_id)
        return c

    def __repr__ (self):
        return "<Colour %s: %s>" % (self._colour_id, self._colour)

    def __str__ (self):
        return self._colour

    def __cmp__ (self, other):
        """
        Allow for rich comparison between colours.

        :``other``: The colour being compared to. Can either be an instance of
                    BaseColour, in which case colour names are compared, or
                    Colour, in which case it attempts to compare colour names
                    with the Colour's current foreground colour.
        """
        if isinstance(other, BaseColour):
            return cmp(self._colour_id, other._colour_id)
        elif isinstance(other, Colour):
            if hasattr(other._foreground, "_colour"):
                return cmp(self._colour_id, other._foreground._colour_id)

        return cmp(self, other)

class ColourLibrary (object):
    """
    A collection of standardised Base colours contained within a specific library.
    """
    _colours = None
    def __init__ (self):
        """
        Initialise the blank library.
        """
        self._colours = []

    def add (self, name, id):
        """
        Include a specific colour in the library.

        :``name``: The name of the colour.
        :``id``: The identifier for the colour.
        """
        colour = BaseColour(name, id)

        self._colours.append(colour)

        setattr(self, name.lower(), colour)
        setattr(self, name.upper(), colour)

    def find (self, name):
        """
        Find a specific colour within the library.

        :``name``: The name of the colour being searched for.
        """
        if hasattr(self, name.lower()):
            return getattr(self, name.lower())

        for colour in self._colours:
            if name in str(colour):
                return colour

        return None

Colours = ColourLibrary()

Colours.add("black", 0)
Colours.add("blue", 1)
Colours.add("green", 2)
Colours.add("cyan", 3)
Colours.add("red", 4)
Colours.add("magenta", 5)
Colours.add("brown", 6)
Colours.add("lightgray", 7)
Colours.add("darkgray", 8)
Colours.add("lightblue", 9)
Colours.add("lightgreen", 10)
Colours.add("lightcyan", 11)
Colours.add("lightred", 12)
Colours.add("lightmagenta", 13)
Colours.add("yellow", 14)
Colours.add("white", 15)

Colors = Colours

class Colour (object):
    """
    A representation of agnostic colours in a variety of configurations:
    individually as either foreground or background colours, combined with
    foreground and background colours, individually as a style, or any
    combination of the previous with a style.
    """
    _foreground = None
    _background = None
    _style = None
    def __init__ (self, foreground=None, background=None, style=None):
        """
        Create a new colour representation.
        """
        assert not (foreground is None and background is None and style is None)

        assert background.is_base() and background in (Colours.BLACK,
            Colours.RED, Colours.GREEN, Colours.BROWN, Colours.BLUE,
            Colours.MAGENTA, Colours.CYAN, Colours.LIGHTGRAY, None)

        assert style in ("bold", "underline", "blink", "standout", None)

        self._foreground = foreground
        self._background = background
        self._style = style

    def __iter__ (self):
        f = self._foreground
        b = self._background
        s = self._style
        if f is None:
            f = DEFAULT
        if b is None:
            b = DEFAULT
        if s is None:
            s = ""

        return (",".join(str(f), str(s)), str(b))
