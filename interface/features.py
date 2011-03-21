#!/usr/bin/env python
"""
features, a short library of specifically defined features.
"""
from library.feature import *
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
FIREPLACE = TextFeature("]", Colours.LIGHTRED, "fireplace", "A fireplace.", False, True)
HEARTH    = TextFeature("]", Colours.LIGHTRED, "hearth", "A hearth.", False, True)
CUPBOARD  = TextFeature("[", Colours.BROWN, "cupboard", "A cupboard.", False, True)
WARDROBE  = TextFeature("[", Colours.BROWN, "wardrobe", "A wardrobe.", False, True)
BOOKSHELF = TextFeature("[", Colours.BROWN, "bookshelf", "A bookshelf.", False, True)
SHELF     = TextFeature("[", Colours.BROWN, "shelf", "A shelf.", False, True)
CHAIR = TextFeature('\\', Colours.BROWN, "chair", "A chair.", True)
TABLE = TextFeature('=', Colours.BROWN, "table", "A table.", False)
DESK = TextFeature('=', Colours.BROWN, "desk", "A desk.", False)
BED = TextFeature('_', Colours.BROWN, "bed", "A bed.", False)

# Plants, etc.
TREE = TextFeature("&", Colours.GREEN, "tree", "A tree.", True)

Features = [FLOOR, GRASS, COBBLES, WALL, CLOSED_DOOR, OPEN_DOOR, WINDOW_V, WINDOW_H,
STAIR_UP, STAIR_DOWN, FIREPLACE, HEARTH, CUPBOARD, WARDROBE, BOOKSHELF, SHELF,
CHAIR, TABLE, DESK, BED, TREE]

def get_furniture_by_name(name):
    for f in Features:
        if f.name() == name:
            return f

    return NOTHING

def feature_is_floor (feat):
    return feat == FLOOR or feat == GRASS or feat == COBBLES

def feature_is_door (feat):
    return feat == OPEN_DOOR or feat == CLOSED_DOOR

def feature_is_stairs (feat):
    return feat == STAIRS_UP or feat == STAIRS_DOWN

def feature_is_window (feat):
    return feat == WINDOW_V or feat == WINDOW_H

def feature_is_container (feat):
    return feat == CUPBOARD or feat == WARDROBE or feat == BOOKSHELF or feat == DESK
