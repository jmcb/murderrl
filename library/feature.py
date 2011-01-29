#!/usr/bin/env python

class Feature (object):
    """
    A way of representing a specific feature in an agnostic manner. This should
    be subclassed for the different interfaces, never used directly.
    """
    _name = None
    _description = None
    _traversable = False

    def __init__ (self, name, description, traversable=False):
        """
        Create a new feature. 

        :``name``: The name of the feature, which will be used when describing the
                   feature upon examination.
        :``description``: This string value will be used to describe the feature
                   upon examination.
        :``traversable``: If True, this glyph is traversable.
        """
        self._name = name
        self._description = description
        self._traversable = traversable

    def traversable (self):
        return self._traversable

    passable = property(lambda self: self.traversable)

    def name (self):
        return self.name

    def description (self):
        return self.description

class TextFeature (Feature):
    """
    A representation of an agnostic ``Feature`` as text. This includes a
    variety of symbols and colours.
    """
    _glyph = None
    _colour = None
    def __init__ (self, glyph=None, colour=None, name="", description="", traversable=False):
        """
        Create a new TextFeature.

        :``glyph``: The glyph used to represent this feature.
        :``colour``: The colour used to colour this feature. Should be an
                     instance of Colour.
        :``name``: The name of this feature.
        :``description``: The description of this feature.
        :``traversable``: Whether or not this glyph can be traversed by the
                          player or non-player characters.
        """
        self._glyph = glyph
        self._colour = colour
        Feature.__init__(self, name=name, description=description, traversable=traversable)

    def glyph (self):
        return self._glyph

    def colour (self):
        return self._colour
