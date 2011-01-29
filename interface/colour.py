#!/usr/bin/env python

class BaseColour (object):
    """
    An agnostic representation of a basic, single-state colour, as used by
    Urwid.
    """
    _colour = None
    def __init__ (self, colour_name):
        """
        Create a new colour.

        :``colour_name``: The representation of the colour.
        """
        self._colour = colour_name

    def is_base (self):
        """
        Determines if this colour is a "base colour", that is, one of the 16
        "allowed" colours that are defined by Urwid. Colours that are not "base"
        are those that are in hexadecimal notation (#fff, for instance)
        """
        if self._colour.startswith("g") or self._colour.startswith("#") or self.colour.startswith("h"):
            return False

        return True

    def __rerp__ (self):
        return "<Colour: %s>" % self._colour

    def __str__ (self):
        return self._colour

BLACK = BaseColour("black")
BLUE = BaseColour("dark blue")
GREEN = BaseColour("dark green")
CYAN = BaseColour("dark cyan")
RED = BaseColour("dark red")
MAGENTA = BaseColour("dark magenta")
BROWN = BaseColour("brown")
LIGHTGRAY = BaseColour("light gray")
LIGHTGREY = LIGHTGRAY
DARKGRAY = BaseColour("dark gray")
DARKGREY = DARKGRAY
LIGHTBLUE = BaseColour("light blue")
LIGHTGREEN = BaseColour("light green")
LIGHTCYAN = BaseColour("light cyan")
LIGHTRED = BaseColour("light red")
LIGHTMAGENTA = BaseColour("light magenta")
YELLOW = BaseColour("yellow")
WHITE = BaseColour("white")
DEFAULT = BaseColour("default")

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

        assert background.is_base() and background in (DEFAULT, BLACK, RED,
            GREEN, BROWN, BLUE, MAGENTA, CYAN, LIGHTGRAY)

        assert style in ("bold", "underline", "blink", "standout")

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
