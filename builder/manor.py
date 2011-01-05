#!/usr/bin/env python
"""
Attempt to create a "manor" akin to:

  ###############################################
  #.........#......#........#.........#.........#
  #.........#......#........#.........#.........#
  #.........#......#........#.........#.........#
  #.........#......#........#.........#.........#
  #########+####+######+###########+###+#########
  #.......+......+......................+.......#
  #.......######+######+#.......#######+#.......#
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......####....+.......#.......#
  #.......#......#......#..+....#.......#.......#
  ##########################....#################
                           ##++##

"""
import sys
sys.path.append("../")
import shape, coord, random, database

# Specific build styles:
ONE_CORRIDOR = "one-corridor"
L_CORRIDOR = "l-corridor"
Z_CORRIDOR = "z-corridor"

class Room (object):
    """
    Currently a builder-only representation of a room.
    """
    def __init__ (self, width=10, height=6, name="", start=None, stop=None):
        """
        Create a room.

        :``width``: The width of the room. *Default 10*.
        :``height``: The height of the room. *Default 6*.
        :``name``: The descriptive name of the room. ie, "Library". *Default ""*.
        :``start``: A coord denoting the top-left point of the room. *Default None*.
        :``stop``: A coord denoting the bottom-right point of the room. *Default None*.

        """
        self.width = width
        self.height = height
        self.name = name
        self.start = start
        self.stop = stop
    def as_shape (self):
        """
        Converts the room into a Shape object, by way of a Box.
        """
        return shape.Box(width=self.width, height=self.height, border=1, fill=".", border_fill="#")

def builder (style=ONE_CORRIDOR):
    """
    Attempts to build a manor based on the style provided. It returns
    ShapeCollection and a list of Room objects.

    :``style``: One of ``ONE_CORRIDOR``, ``L_CORRIDOR`` or ``Z_CORRIDOR``.
                Currently on ``ONE_CORRIDOR`` is supported. *Default
                ONE_CORRIDOR*.
    """
    room_names = data.rooms.copy()

    rooms = []

    if style == ONE_CORRIDOR:
        # Top row of rooms
        row1 = []
        # Corridor, then bottom row of rooms
        row2 = []

        # We start with the entrance hall and add rooms on either side of it
        # until we have a minimum of six and a maximum of ten
        entrance_hall = Room()

        row2.append(entrance_hall)

        while len(row2) >= 10:
            # If we have six rooms, one in three chance of not adding any more
            # rooms.
            if len(row2) < 6 and random.randint(1, 3) == 1:
                break


    else:
        return shape.ShapeCollection(), rooms
