#!/usr/bin/env python
"""
Attempt to create a "manor" akin to::

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
import random, copy, room, manor
from library import shape, collection
from library.coord import *
from library.random_util import *
from library.feature import *

# Specific build styles:
BASE_SHAPE = "single-corridor"
L_LAYOUT = "L-corridors"
Z_LAYOUT = "Z-corridors"
N_LAYOUT = "N-corridors"
H_LAYOUT = "H-corridors"
O_LAYOUT = "O-corridors"
U_LAYOUT = "U-corridors"

class Corridor (shape.Shape):
    pass

class MainCorridor (Corridor):
    pass

def base_builder ():
    """
    Attempts to build a manor based on the style provided. It returns
    ShapeCollection and a list of Room objects.

    :``style``: One of ``ONE_CORRIDOR``, ``L_CORRIDOR`` or ``Z_CORRIDOR``.
                Currently on ``ONE_CORRIDOR`` is supported. *Default
                ONE_CORRIDOR*.
    """
    # Top row of rooms
    row1 = []
    # Corridor, then bottom row of rooms
    row2 = []

    # We start with the entrance hall and add rooms on either side of it
    # until we have a minimum of six and a maximum of ten
    entrance_hall = room.Room()

    left  = 0
    right = 0

    row2.append(entrance_hall)

    while len(row2) <= 5:
        # If we have six rooms, one in three chance of not adding any more
        # rooms.
        if len(row2) > 4 and one_chance_in(3):
            break

        new_room = room.Room()

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
        new_room = room.Room()
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
        row2[0].height  += 2
        row2[-1].height += 2
        row1[0].width   += 2
        row1[-1].width  += 2
        row2[1].width   += 2
        row2[-2].width  += 2
    elif adjust_bottom == 1:
        side_adjusted = random.randint(-1, 0)
        side_not_adjusted = -side_adjusted-1
        row2[side_adjusted].height     += 2
        row1[side_not_adjusted].height += 2
        row2[side_not_adjusted].width  += 2
        row1[side_adjusted].width      += 2
    elif adjust_bottom == 0:
        overlap = 3
        row1[0].height  += 2
        row1[-1].height += 2
        row2[0].width   += 2
        row2[-1].width  += 2
        row1[1].width   += 2
        row1[-2].width  += 2

    # Now, start drawing it! YAY!

    # First row
    first_room  = row1[0].as_shape()
    second_room = row1[1].as_shape()
    row1_collection = shape.adjoin(first_room, second_room, overlap=1, collect=True)
    for curr in row1[2:]:
        row1_collection = shape.adjoin(row1_collection, curr.as_shape(), overlap=1, collect=True)

    # second row
    first_room  = row2[0].as_shape()
    second_room = row2[1].as_shape()

    # Does some weird stuff to offset everything
    offset_both = False
    if first_room.height() == second_room.height():
        offset_both = True

    row2_collection = shape.adjoin(first_room, second_room, top_offset=top_offset, overlap=1, collect=True, offset_both=offset_both)
    for curr in row2[2:]:
        to = top_offset
        room_shape = curr.as_shape()
        if room_shape.height() == first_room.height() and not offset_both or room_shape.height() > first_room.height():
            to = 0
        row2_collection = shape.adjoin(row2_collection, room_shape, top_offset=to, overlap=1, collect=True)

    # Finally, make a corridor!
    room_width  = room.Room().width
    room_height = room.Room().height

    my_collection = shape.underneath(row1_collection, row2_collection, overlap=overlap, collect=True)
    m = manor.ManorCollection(my_collection)

    corridor_length = my_collection.width() - room_width * 2
    corridor = MainCorridor(shape.Row(width=corridor_length, fill="."))

    m.append(collection.ShapeCoord(corridor, coord.Coord(room_width, room_height)))

    return m

class Placement (object):
    def __init__ (self, side1, side2, this_side):
        self.sides = [side1, side2]
        self.this_side = this_side
    def opposite (self):
        return self.sides[self.this_side-1]
    def __hash__ (self):
        return hash(str(self))
    def __str__ (self):
        return self.sides[self.this_side]
    def __repr__ (self):
        return "<Placement %s>" % self
    def __cmp__ (self, other):
        return cmp(str(self), str(other))

SIDE_LEFT    = Placement("left", "right", 0)
SIDE_RIGHT   = Placement("left", "right", 1)
PLACE_TOP    = Placement("top", "bottom", 0)
PLACE_BOTTOM = Placement("top", "bottom", 1)

class Leg (object):
    def __init__ (self, h_placement, v_placement, width=None, height=None, leg=None):
        assert not (leg is None and width is None and height is None)

        if leg is not None:
            width, height = leg.size()

        self.placement = (h_placement, v_placement)
        self.width  = width
        self.height = height
    def __repr__ (self):
        return "<Leg h:%s w:%s %s>" % (self.height, self.width, self.placement)
    def __cmp__ (self, other):
        if isinstance(other, Leg):
            return cmp(self.placement, other.placement)
        elif isinstance(other, tuple):
            return cmp(self.placement, other)

def attach_leg (base, leg, side=SIDE_LEFT, placement=PLACE_TOP):
    """
    Take a result of base_builder() and attach a leg.

    :``base``: The base shape collection.
    :``leg``: The leg shape collection.
    :``side``: Which side the leg should be placed on. *Default SIDE_LEFT*.
    :``placement``: Whether the leg should be placed above or below. *Default PLACE_TOP*.
    """
    assert not base.leg_at(side, placement)

    old_leg = leg.copy()

    no_vert_offset = False
    vert_offset = 0

    if base.leg_at(side.opposite(), placement):
        l = base.get_leg(side.opposite(), placement)
        vert_offset = base.height() - l.height
        no_vert_offset = True
    else:
        vert_offset = base.height() - 1

    # Find the corridor
    corridor, start = base.corridor(base.main_corridor)
    assert corridor is not None

    # Find the corridor's starting point
    stop   = coord.Coord(start)
    stop.x = corridor.width()

    if side == SIDE_LEFT:
        leg.offset(coord.Coord(stop.x-1, 0))
        y_offset = stop.x + (room.Room().width - 1)
    elif side == SIDE_RIGHT:
        y_offset = start.x

    new_corridor = Corridor(shape.Column(height=leg.height() + room.Room().height, fill="."))

    corridor_offset = None

    if placement == PLACE_BOTTOM:
        if no_vert_offset:
            base.place_on(leg, offset=coord.Coord(0, vert_offset))
        else:
            base = shape.underneath(base, leg, overlap=1, collect=True)
        new_corridor[coord.Coord(0, new_corridor.height()-1)] = "#"
        corridor_offset = coord.Coord(y_offset, vert_offset - room.Room().height)
        base.append(new_corridor, corridor_offset)
    elif placement == PLACE_TOP:
        if no_vert_offset:
            base.place_on(leg)
        else:
            base = shape.underneath(leg, base, overlap=1, collect=True)
        new_corridor[POS_ORIGIN] = "#"
        corridor_offset = coord.Coord(y_offset, 0)
        base.append(new_corridor, corridor_offset)

    if placement == PLACE_TOP:
        start = coord.Coord(corridor_offset.x - 1, leg.height() - 1)
    elif placement == PLACE_BOTTOM:
        start = coord.Coord(corridor_offset.x - 1, vert_offset - room.Room().height + 1)

    new_shape = shape.Shape(width=3, height=room.Room().height, fill="#")
    new_shape.draw_on(shape.Shape(width=1, height=room.Room().height, fill="."), offset=DIR_EAST, check_conflict=False)

    base = manor.ManorCollection(base)

    base.draw_on(new_shape, start)
    base.mark_leg(Leg(side, placement, leg=old_leg))

    return base

def build_leg (rooms_tall=2, rooms_wide=2, make_corridor=True, do_cleanup=True):
    """
    Create and return a "leg" to be used with add_leg.

    :``rooms_tall``: How many rooms tall to make the leg. *Default 2*.
    :``rooms_wide``: How many rooms wide to make the leg. *Max 2. Default 2*.
    :``make_corridor``: Include a corridor when building. *Default True*.
    :``do_cleanup``: Perform corridor, etc, clean-up when built. *Default True*.
    """
    assert rooms_wide >= 1 and rooms_wide <= 2
    assert rooms_tall >= 1
    new_rooms = collection.ShapeCollection()

    for row in xrange(rooms_tall):
        rooms = []
        for r in xrange(rooms_wide):
            rooms.append(room.Room().as_shape())

        this_row = collection.ShapeCollection()
        this_row = shape.adjoin(rooms.pop(), this_row, overlap=-1, collect=True)

        for r in rooms:
            this_row = shape.adjoin(this_row, r, overlap=-1, collect=True)

        new_rooms = shape.underneath(this_row, new_rooms, overlap=1, collect=True)

    return new_rooms

def build_L (base=None, rooms=2, rooms_wide=2):
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
    new_rooms = build_leg(rooms, rooms_wide)

    side = random.choice([SIDE_LEFT, SIDE_RIGHT])
    placement = random.choice([PLACE_TOP, PLACE_BOTTOM])

    base = attach_leg(base, new_rooms, side=side, placement=placement)
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

    base = build_U(base, placement=PLACE_TOP)
    base = build_U(base, placement=PLACE_BOTTOM)

    return base

def build_O (base=None):
    if base is None:
        base = base_builder()
    return base

def build_U (base=None, rooms=2, rooms_wide=2, placement=None):
    if base is None:
        base = base_builder()

    # Draw the new rooms.
    new_rooms1 = build_leg(rooms, rooms_wide)
    new_rooms2 = build_leg(rooms, rooms_wide)

    if placement is None:
        placement = random.choice([PLACE_TOP, PLACE_BOTTOM])

    base = attach_leg(base, new_rooms1, side=SIDE_LEFT, placement=placement)
    base = attach_leg(base, new_rooms2, side=SIDE_RIGHT, placement=placement)
    return base

def builder_by_type (type = None):
    if type == None:
        return build_random()
    if type == 'B':
        return base_builder()
    if type == 'L':
        return build_L()
    if type == 'U':
        return build_U()
    if type == 'H':
        return build_H()
    # The other types don't exist yet and fall back on the base_builder.
    if type == 'O':
        return build_O()
    if type == 'N':
        return build_N()
    if type == 'Z':
        return build_Z()
    else:
        return base_builder()

def build_random (base=None):
	l_list = [L_LAYOUT, Z_LAYOUT, N_LAYOUT, H_LAYOUT, O_LAYOUT, U_LAYOUT]
	layout = random.choice(l_list)

	if layout == L_LAYOUT:
		return build_L(base)
	elif layout == Z_LAYOUT:
		return build_Z(base)
	elif layout == N_LAYOUT:
		return build_N(base)
	elif layout == H_LAYOUT:
		return build_H(base)
	elif layout == O_LAYOUT:
		return build_O(base)
	elif layout == U_LAYOUT:
		return build_U(base)
	else:
		return base_builder()
