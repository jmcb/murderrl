#!/usr/bin/env python

from library import coord

class Feature (object):
    """
    A way of representing a specific feature in an agnostic manner. This should
    be subclassed for the different interfaces, never used directly.
    """
    _name = None
    _description = None
    _traversable = False

    def __init__ (self, name, description=None, traversable=False, needs_wall=False, is_container=False):
        """
        Create a new feature. 

        :``name``: The name of the feature, which will be used when describing the
                   feature upon examination.
        :``description``: This string value will be used to describe the feature
                   upon examination.
        :``traversable``: If True, this glyph is traversable. *Default False*.
        :``needs_wall``: If True, may only be placed adjacent to a wall. *Default False*.
        :``is_container``: If True, searching may provide a clue. *Default False*.
        """
        self._name = name
        if description == None:
            description = "A %s." % name
        self._description  = description
        self._traversable  = traversable
        self._needs_wall   = needs_wall
        self._is_container = is_container

    def traversable (self):
        return self._traversable

    passable = property(lambda self: self.traversable)

    def name (self, needs_article=False):
        if needs_article and not self._has_article:
            return "a %s" % self._name
        return self._name

    def description (self):
        return self._description

    def needs_wall (self):
        return self._needs_wall

    def is_container (self):
        return self._is_container

class TextFeature (Feature):
    """
    A representation of an agnostic ``Feature`` as text. This includes a
    variety of symbols and colours.
    """
    _glyph = None
    _colour = None
    def __init__ (self, glyph=None, colour=None, name="", description="", traversable=False, needs_wall=False, is_container=False):
        """
        Create a new TextFeature.

        :``glyph``: The glyph used to represent this feature. *Default none*.
        :``colour``: The colour used to colour this feature. Should be an
                     instance of Colour. *Default none*.
        :``name``: The name of this feature. *Default empty*.
        :``description``: The description of this feature. *Default empty*.
        :``traversable``: Whether or not this glyph can be traversed by the
                          player or non-player characters. *Default False*.
        :``needs_wall``: If True, may only be placed adjacent to a wall. *Default False*.
        :``is_container``: If True, searching may provide a clue. *Default False*.
        """
        self._glyph  = glyph
        self._colour = colour
        self._has_article = False
        Feature.__init__(self, name=name, description=description, traversable=traversable, needs_wall=needs_wall, is_container=False)

    def glyph (self):
        return self._glyph

    def colour (self):
        return self._colour

    def derived_feature (self, name=None, desc=None, glyph=None, colour=None, traversable=None, needs_wall=None, is_container=None):
        if name == None:
            name = self.name()
        if desc == None:
            desc = "A %s." % name
        if glyph == None:
            glyph = self.glyph()
        if colour == None:
            colour = self.colour()
        if traversable == None:
            traversable = self.traversable()
        if needs_wall == None:
            needs_wall = self.needs_wall()
        if is_container == None:
            is_container = self.is_container()

        new_feat = TextFeature(glyph, colour, name, desc, traversable, needs_wall, is_container)
        return new_feat

NOTHING = TextFeature(" ", None, "nothingness", "Empty space.", False)

class FeatureGrid (object):
    """
    A grid of Features at various positions.
    """
    def __init__ (self, width, height, feat = NOTHING):
        """
        Create a new FeatureGrid.

        :``width``: The width of the grid. *Required*.
        :``height``: The height of the grid. *Required*.
        :``feat``: The default feature used to initialise the grid. *Default NOTHING*.
        """
        self.grid = []
        self._width  = width
        self._height = height
        for row in xrange(height):
            row = []
            for column in xrange(width):
                row.append(feat)
            self.grid.append(row)

    def size (self):
        """
        Returns the size of the grid.
        """
        return coord.Coord(self._width, self._height)

    def __getitem__ (self, pos):
        """
        Returns the Feature at a given position.

        :``pos``: A position within the grid. *Required*.
        """
        # assert isinstance(pos, coord.Coord)
        assert (pos.y < self._height)
        assert (pos.x < self._width)
        return self.grid[pos.y][pos.x]

    def __setitem__ (self, pos, feat):
        """
        Updates the Feature at a given position.

        :``pos``: A position within the grid. *Required*.
        :``feat``: The new feature for this position. *Required*.
        """
        # assert isinstance(pos, coord.Coord)
        assert (pos.y < self._height)
        assert (pos.x < self._width)
        self.grid[pos.y][pos.x] = feat

    def draw (self):
        """
        Prints the feature glyphs onto the screen. Debugging method.
        """
        canvas = []
        for x in xrange(self._height):
            row = []
            for y in xrange(self._width):
                glyph = self.__getitem__(coord.Coord(y, x)).glyph()
                row.append(glyph)
            print ''.join(row)
