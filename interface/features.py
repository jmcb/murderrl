#!/usr/bin/env python
"""
features, a short library of specifically defined features.
"""
from library.feature import TextFeature
from library.colour import Colours

WALL = TextFeature("#", Colours.WHITE)
FLOOR = TextFeature(".", Colours.LIGHTGRAY)
DOOR = TextFeature("+", Colours.WHITE)
STAIR_UP = TextFeature("<", Colours.WHITE)
STAIR_DOWN = TextFeature(">", Colours.WHITE)
WINDOW_V = TextFeature("|", Colours.WHITE)
WINDOW_H = TextFeature("-", Colours.WHITE)
TREE = TextFeature("&", Colours.GREEN)
