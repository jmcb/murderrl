#!/usr/bin/env python
"""
features, a short library of specifically defined features.
"""
from library.feature import TextFeature
from library.colour import Colours

# Floor-related glyphs.
FLOOR = TextFeature(".", Colours.LIGHTGRAY, "floor", "Floor.", True)
GRASS = TextFeature(".", Colours.GREEN, "grass", "Grass.", True)
COBBLES = TextFeature(",", Colours.BROWN, "cobbles", "Cobblestones.", True)

# Wall-related glyphs.
WALL = TextFeature("#", Colours.WHITE, "wall", "A wall.", False)
# For simplicity's sake, doors are currently considered traversable even
# when closed. Opening doors is implied, okay? (jpeg)
CLOSED_DOOR = TextFeature("+", Colours.WHITE, "closed door", "A closed door.", True)
OPEN_DOOR = TextFeature("'", Colours.WHITE, "open door", "An open door.", True)
WINDOW_V = TextFeature("|", Colours.WHITE, "window", "A window.", False)
WINDOW_H = TextFeature("-", Colours.WHITE, "window", "A window.", False)

# Stairs.
STAIR_UP = TextFeature("<", Colours.WHITE, "stairs up", "A staircase leading up.", True)
STAIR_DOWN = TextFeature(">", Colours.WHITE, "stairs down", "A staircase leading down.", True)

# Furniture
FIREPLACE = TextFeature("]", Colours.LIGHTRED, "fireplace", "A fireplace.", False)
CUPBOARD = TextFeature("[", Colours.BROWN, "cupboard", "A cupboard.", False)
CHAIR = TextFeature('\\', Colours.BROWN, "chair", "A chair.", True)
TABLE = TextFeature('=', Colours.BROWN, "table", "A table.", False)
DESK = TextFeature('=', Colours.BROWN, "desk", "A desk.", False)

# Plants, etc.
TREE = TextFeature("&", Colours.GREEN, "tree", "A tree.", True)
