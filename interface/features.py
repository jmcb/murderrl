#!/usr/bin/env python
"""
features, a short library of specifically defined features.
"""
from library.feature import *
from library.colour import Colours

# Floor-related glyphs.
FLOOR   = TextFeature(".", Colours.LIGHTGRAY, "floor", "Floor.", traversable=True)
GRASS   = FLOOR.derived_feature("grass", "Grass.", colour=Colours.GREEN)
COBBLES = FLOOR.derived_feature("cobbles", "Cobblestones.", glyph=",", colour=Colours.BROWN)

# Wall-related glyphs.
WALL = TextFeature("#", Colours.LIGHTGRAY, "wall", traversable=False)

# For simplicity's sake, doors are currently considered traversable even
# when closed. Opening doors is implied, okay? (jpeg)
CLOSED_DOOR = TextFeature("+", Colours.LIGHTGRAY, "closed door", traversable=True)
OPEN_DOOR   = CLOSED_DOOR.derived_feature("open door", "An open door.", glyph="'")
LOCKED_DOOR = CLOSED_DOOR.derived_feature("locked door", traversable=False)
PORTAL      = CLOSED_DOOR.derived_feature("entrance door", colour=Colours.BROWN, traversable=False)

# Windows
WINDOW_V = TextFeature("|", Colours.LIGHTCYAN, "window", traversable=False)
WINDOW_H = WINDOW_V.derived_feature(glyph="-")

# Stairs.
STAIR_UP   = TextFeature("<", Colours.WHITE, "stairs up", "A staircase leading up.", traversable=True)
STAIR_DOWN = STAIR_UP.derived_feature("stairs down", "A staircase leading down.", glyph=">")

# Furniture
FIREPLACE = TextFeature("]", Colours.YELLOW, "fireplace", traversable=False, needs_wall=True)
HEARTH    = FIREPLACE.derived_feature("hearth")

# Cupboards
CUPBOARD  = TextFeature("[", Colours.BROWN, "cupboard", traversable=False, needs_wall=True, is_container=True)
WARDROBE  = CUPBOARD.derived_feature("wardrobe")
BOOKSHELF = CUPBOARD.derived_feature("bookshelf")
SHELF     = CUPBOARD.derived_feature("shelf")

# Tables
TABLE          = TextFeature('=', Colours.BROWN, "table", traversable=False)
DESK           = TABLE.derived_feature("desk", is_container=True)
DINING_TABLE   = TABLE.derived_feature("large table")
BILLIARD_TABLE = TABLE.derived_feature("billiard table", colour=Colours.GREEN)
WORK_TABLE     = TABLE.derived_feature("work table")
PIANO          = TABLE.derived_feature("piano", colour=Colours.WHITE)

# Chairs
CHAIR = TextFeature('\\', Colours.BROWN, "chair", traversable=True)
STOOL = CHAIR.derived_feature("stool")

BED   = TextFeature('_', Colours.WHITE, "bed", traversable=False)

# Plants, etc.
TREE = TextFeature("&", Colours.GREEN, "tree", traversable=False)

# Corpse of the victim, immovable item -> might as well be a feature
BODY = TextFeature("X", Colours.RED, "body", "The victim's body.", traversable=True)

# Features that can be added within rooms as furniture.
Features = [STAIR_UP, STAIR_DOWN, FIREPLACE, HEARTH, CUPBOARD, WARDROBE, BOOKSHELF, SHELF,
TABLE, DINING_TABLE, BILLIARD_TABLE, WORK_TABLE, DESK, PIANO, CHAIR, STOOL, BED, TREE]

def get_furniture_by_name(name):
    for f in Features:
        if f.name() == name:
            return f

    return NOTHING

def feature_is_floor (feat):
    return feat == FLOOR or feat == GRASS or feat == COBBLES

def feature_is_door (feat):
    return feat == OPEN_DOOR or feat == CLOSED_DOOR or feat == LOCKED_DOOR

def feature_is_stairs (feat):
    return feat == STAIRS_UP or feat == STAIRS_DOWN

def feature_is_window (feat):
    return feat == WINDOW_V or feat == WINDOW_H

def feature_is_large_table (feat):
    return feat == WORK_TABLE or feat == DINING_TABLE or feat == BILLIARD_TABLE
