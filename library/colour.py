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
        are those that are in hexadecimal notation (#fff, for instance),
        grey-scale notation (g40, g#cc, for instance), or specific colour
        numbers (h8, for instance).
        """
        if self._colour.startswith("g") or self._colour.startswith("#") or self.colour.startswith("h"):
            return False

        return True

    def lighten (self):
        """
        Performs an in-place lightening of the current colour. This function can
        only be currently applied to colours that return True for ``is_base()``.
        """
        if "dark" in self._colour:
            self._colour = self._colour.replace("dark", "light")
        else:
            if self._colour == "brown":
                self._colour = "yellow"
            elif self._colour == "light gray":
                self._colour = "white"

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
        if "light" in self._colour:
            self._colour = self._colour.replace("light", "dark")
        else:
            if self._colour == "yellow":
                self._colour = "brown"
            elif self._colour == "white":
                self._colour = "light gray"

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
        c = BaseColour(self._colour)
        return c

    def __rerp__ (self):
        return "<Colour: %s>" % self._colour

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
            return cmp(self._colour, other._colour)
        elif isinstance(other, Colour):
            if hasattr(other._foreground, "_colour"):
                return cmp(self._colour, other._foreground._colour)

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

    def add (self, name, colour=None):
        """
        Include a specific colour in the library.

        :``name``: The name of the colour.
        :``colour``: An instance of BaseColour. If ``None``, a new BaseColour
                     will be initialised using ``name`` as the colour name.
        """
        if colour is None:
            colour = BaseColour(name)

        if not isinstance(colour, BaseColour):
            colour = BaseColour(colour)

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

Colours.add("black")
Colours.add("blue", "dark blue")
Colours.add("green", "dark green")
Colours.add("cyan", "dark cyan")
Colours.add("red", "dark red")
Colours.add("magenta", "dark magenta")
Colours.add("brown")
Colours.add("lightgray", "light gray")
Colours.add("lightgrey", "light gray")
Colours.add("darkgray", "dark gray")
Colours.add("darkgrey", "dark gray")
Colours.add("lightblue", "light blue")
Colours.add("lightblue", "light green")
Colours.add("lightcyan", "light cyan")
Colours.add("lightred", "light red")
Colours.add("lightmagenta", "light magenta")
Colours.add("yellow")
Colours.add("white")
Colours.add("default")

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

        assert background.is_base() and background in (Colours.DEFAULT,
           Colours.BLACK, Colours.RED, Colours.GREEN, Colours.BROWN, Colours.BLUE,
            Colours.MAGENTA, Colours.CYAN, Colours.LIGHTGRAY)

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
