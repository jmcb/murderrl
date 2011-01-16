#!/usr/bin/env python
"""
Attempt to create a "manor" akin to:

  ###############################################
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #########+####+######+###########+#####.......#
  #.......+......+......................+.......#
  #.......######+######+#.......#######+#########
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......####....+.......#.......#
  #.......#......#......#..+....#.......#.......#
  ##########################....#################
                           ##++##

"""

import random
from library import shape, coord, collection
from database import database

# Specific build styles:
BASE_SHAPE = "single-corridor"
L_LAYOUT = "L-corridors"
Z_LAYOUT = "Z-corridors"
N_LAYOUT = "N-corridors"
H_LAYOUT = "H-corridors"
O_LAYOUT = "O-corridors"

class Room (object):
    """
    Currently a builder-only representation of a room.
    """
    def __init__ (self, width=12, height=7, start=None, stop=None):
        """
        Create a room.

        :``width``: The width of the room. *Default 10*.
        :``height``: The height of the room. *Default 6*.
        :``start``: A coord denoting the top-left point of the room. *Default None*.
        :``stop``: A coord denoting the bottom-right point of the room. *Default None*.

        """
        self.width = width
        self.height = height
        self.start = start
        self.stop = stop
    def as_shape (self):
        """
        Converts the room into a Shape object, by way of a Box.
        """
        return shape.Box(width=self.width, height=self.height, border=1, fill=".", border_fill="#")
    def __repr__ (self):
        return "<Room width=%s,height=%s,name=%s,start=%s,stop=%s>" % (self.width,self.height,self.name,self.start,self.stop)

def base_builder ():
    """
    Attempts to build a manor based on the style provided. It returns
    ShapeCollection and a list of Room objects.

    :``style``: One of ``ONE_CORRIDOR``, ``L_CORRIDOR`` or ``Z_CORRIDOR``.
                Currently on ``ONE_CORRIDOR`` is supported. *Default
                ONE_CORRIDOR*.
    """
    room_names = database.rooms.copy()

    rooms = []

    # Top row of rooms
    row1 = []
    # Corridor, then bottom row of rooms
    row2 = []

    # We start with the entrance hall and add rooms on either side of it
    # until we have a minimum of six and a maximum of ten
    entrance_hall = Room()

    left = 0
    right = 0

    row2.append(entrance_hall)

    while len(row2) <= 5:
        # If we have six rooms, one in three chance of not adding any more
        # rooms.
        if len(row2) > 4 and random.randint(1, 4) == 1:
            break

        new_room = Room()

        if left > right:
            row2.append(new_room)
            right += 1
        elif left < right:
            row2.insert(0, new_room)
            left += 1
        else:
            side = random.randint(-1, 0)
            if side == -1:
                right += 1
            else:
                left += 1
            row2.insert(side, new_room)

    while len(row1) < len(row2):
        new_room = Room()
        row1.append(new_room)

    # Now, adjust the rooms at either end to compensate for the corridor:
    # 1. We can adjust two rooms on the bottom level for height, 2 on the
    #    top for width.
    # 2. We can adjust one on the bottom and one on the top for height, and
    #    the opposites for width.
    # 3. We can adjust two rooms on the top level for height, 2 on the
    #    bottom for width.
    adjust_bottom = random.randint(0, 2)
    top_offset = 2
    overlap = 3
    if adjust_bottom == 2:
        overlap = 1
        row2[0].height += 2
        row2[-1].height += 2
        row1[0].width += 2
        row1[-1].width += 2
        row2[1].width += 2
        row2[-2].width += 2
    elif adjust_bottom == 1:
        side_adjusted = random.randint(-1, 0)
        side_not_adjusted = -side_adjusted-1
        row2[side_adjusted].height += 2
        row1[side_not_adjusted].height += 2
        row2[side_not_adjusted].width += 2
        row1[side_adjusted].width += 2
    elif adjust_bottom == 0:
        overlap = 3
        row1[0].height += 2
        row1[-1].height += 2
        row2[0].width += 2
        row2[-1].width += 2
        row1[1].width += 2
        row1[-2].width += 2

    # Now, start drawing it! YAY!

    # First row
    first_room = row1[0].as_shape()
    second_room = row1[1].as_shape()
    row1_collection = shape.adjoin(first_room, second_room, overlap=1, collection=True)
    for room in row1[2:]:
        row1_collection = shape.adjoin(row1_collection, room.as_shape(), overlap=1, collection=True)

    # second row
    first_room = row2[0].as_shape()
    second_room = row2[1].as_shape()

    # Does some weird stuff to offset everything
    offset_both = False
    if first_room.height() == second_room.height():
        offset_both = True

    row2_collection = shape.adjoin(first_room, second_room, top_offset=top_offset, overlap=1, collection=True, offset_both=offset_both)
    for room in row2[2:]:
        to = top_offset
        room_shape = room.as_shape()
        if room_shape.height() == first_room.height() and not offset_both or room_shape.height() > first_room.height():
            to = 0
        row2_collection = shape.adjoin(row2_collection, room_shape, top_offset=to, overlap=1, collection=True)

    # Finally, make a corridor!
    room_width = Room().width
    room_height = Room().height

    collection = shape.underneath(row1_collection, row2_collection, overlap=overlap, collection=True)

    corridor_length = collection.width() - room_width * 2
    corridor = shape.Row(width=corridor_length, fill=".")

    collection.append(shape.ShapeCoord(corridor, coord.Coord(room_width, room_height)))

    return collection

BASE_SHAPE = "single-corridor"
L_LAYOUT = "L-corridors"
Z_LAYOUT = "Z-corridors"
N_LAYOUT = "N-corridors"
H_LAYOUT = "H-corridors"
O_LAYOUT = "O-corridors"

def build_L (base=None, rooms=2, rooms_wide=1):
    """
    Modifies the results of base_builder() to result in an L shape in any
    orientation.

    :``base``: The base shape collection. If None, a new base will be built from
               base_builder. *Default None*.
    :``rooms``: How many rooms to build along the sides of the new axis.
    """
    if base is None:
        base = base_builder()

    # Draw the new rooms.
    new_rooms = collection.ShapeCollection()

    for row in xrange(rooms):
        if rooms_wide == 2:
            room1 = Room().as_shape()
            room2 = Room().as_shape()
            this_row = shape.adjoin(room1, room2, overlap=-1, collection=True)
        else:
            this_row = collection.ShapeCollection()
            this_row.append(Room().as_shape())

        new_rooms = shape.underneath(this_row, new_rooms, overlap=1, collection=True)

    # Find the corridor
    corridor = None

    for s in base:
        if s.height() == 1:
            corridor = s
            break

    assert corridor is not None
    corridor, start = corridor

    stop = coord.Coord(start)
    stop.x = corridor.width()

    side = random.choice(["left", "right"])

    y_offset = 0

    # Pick either the right or left end of the corridor.

    if side == "right":
        new_rooms.offset(coord.Coord(stop.x-1, 0))
        y_offset = stop.x + (Room().width - 1)
    else:
        y_offset = start.x

    new_corridor = shape.Column(height=Room().height * (rooms + 1) - (rooms - 1), fill=".")

    corridor_offset = None

    vert = None

    if random.randint(1, 2) == 1:
        base = shape.underneath(base, new_rooms, overlap=1, collection=True)
        new_corridor[coord.Coord(0, new_corridor.height()-1)] = "#"
        corridor_offset = coord.Coord(y_offset, Room().height)
        base.append(new_corridor, corridor_offset)
        vert = "bottom"
    else:
        base = shape.underneath(new_rooms, base, overlap=1, collection=True)
        new_corridor[coord.Coord(0, 0)] = "#"
        corridor_offset = coord.Coord(y_offset, 0)
        base.append(new_corridor, corridor_offset)
        vert = "top"

    # Finally, fixup the broken wall.
    start = None

    if vert == "top":
        start = coord.Coord(corridor_offset.x - 1, Room().height * rooms - rooms)
    else:
        start = coord.Coord(corridor_offset.x - 1, Room().height + 1)

    new_shape = shape.Shape(width=3, height=Room().height, fill="#")
    new_shape.draw_on(shape.Shape(width=1, height=Room().height, fill="."), offset=coord.Coord(1, 0), check_conflict=False)

    base.append(new_shape, start)
    return base

def build_Z (base=None):
    if base is None:
        base = base_builder()
    return base

def build_N (base=None):
    if base is None:
        base = base_builder()
    return base

def build_H (base=None):
    if base is None:
        base = base_builder()
    return base

def build_O (base=None):
    if base is None:
        base = base_builder()
    return base

