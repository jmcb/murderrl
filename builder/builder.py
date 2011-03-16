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
import random, copy, room
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

class BuilderCollection (collection.ShapeCollection):
    corridors = None
    rooms     = None
    legs      = None
    main_corridor = None

    def __init__ (self, c=[]):
        if c != [] and isinstance(c, BuilderCollection):
            self.legs = c.legs

        collection.ShapeCollection.__init__(self, c)
        self.rebuild()

    def copy (self):
        my_copy = BuilderCollection(copy.copy(self._shapes))
        my_copy.legs = copy.deepcopy(self.legs)
        return my_copy

    def rebuild (self):
        self.corridors = []
        self.rooms = []
        if not self.legs:
            self.legs = []
        for index, sh in enumerate(self):
            if isinstance(sh.shape, MainCorridor):
                self.main_corridor = index

            if isinstance(sh.shape, Corridor):
                self.corridors.append(index)
            else:
                self.rooms.append(index)

    def corridor (self, index):
        assert index in self.corridors
        return self[index]

    def get_corridors (self):
        return self.corridors

    def get_room (self, index):
        assert index in self.rooms
        return self[index]

    def get_rooms (self):
        if not self.rooms:
            return None
        return self.rooms

    def mark_leg (self, leg):
        self.legs.append(leg)

    def count_legs (self):
        return len(self.legs)

    def leg_at (self, side, placement):
        return (side, placement) in self.legs

    def get_leg (self, side, placement):
        for leg in self.legs:
            if leg == (side, placement):
                return leg

        return None

    def _rebuild_wrap (function):
        def wrapper (self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.rebuild()
        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__ + "\n\nCalling this function automatically rebuilds the BuilderCollection index."
        return wrapper

    __setitem__ = _rebuild_wrap(collection.ShapeCollection.__setitem__)
    append      = _rebuild_wrap(collection.ShapeCollection.append)
    extend      = _rebuild_wrap(collection.ShapeCollection.extend)
    insert      = _rebuild_wrap(collection.ShapeCollection.insert)
    pop         = _rebuild_wrap(collection.ShapeCollection.pop)
    prioritise  = _rebuild_wrap(collection.ShapeCollection.prioritise)
    reverse     = _rebuild_wrap(collection.ShapeCollection.reverse)
    reversed    = _rebuild_wrap(collection.ShapeCollection.reversed)
    sort        = _rebuild_wrap(collection.ShapeCollection.sort)
    append      = _rebuild_wrap(collection.ShapeCollection.append)
    prioritise  = _rebuild_wrap(collection.ShapeCollection.prioritise)

class Corridor (shape.Shape):
    pass

class MainCorridor (Corridor):
    pass

def join_row_rooms (row, left=False, right=False, check_offset=False):
    assert(len(row) > 2)

    first_room  = row[0].as_shape()
    second_room = row[1].as_shape()

    # Does some weird stuff to offset everything
    offset_both = False
    if check_offset and first_room.height() == second_room.height():
        offset_both = True

    # Join the first two rooms.
    top_offset = 0
    if check_offset:
        top_offset = 2
    overlap = 1
    if left:
        overlap = -1
    row_collection = shape.adjoin(first_room, second_room, top_offset=top_offset, overlap=overlap, collect=True, offset_both=offset_both)

    # Join the middle rooms.
    for curr in row[2:-1]:
        room_shape = curr.as_shape()
        to = top_offset
        if check_offset and (room_shape.height() == first_room.height() and not offset_both or room_shape.height() > first_room.height()):
            to = 0
        row_collection = shape.adjoin(row_collection, room_shape, top_offset=to, overlap=1, collect=True, offset_both=offset_both)

    # Join the last room.
    last_room = row[-1].as_shape()
    if check_offset and (last_room.height() == first_room.height() and not offset_both or last_room.height() > first_room.height()):
        top_offset = 0
    overlap = 1
    if right:
        overlap = -1
    row_collection = shape.adjoin(row_collection, last_room, top_offset=top_offset, overlap=overlap, collect=True)
    return row_collection

ROOM_WIDTH_LIST = [7, 8, 9, 10, 11, 12]

def base_builder (top_left=None, top_right=None, bottom_left=None, bottom_right=None, tl_corr=False, tr_corr=False, bl_corr=False, br_corr=False):
    """
    Attempts to build a manor based on the style provided. It returns
    ShapeCollection and a list of Room objects.

    :``style``: One of ``ONE_CORRIDOR``, ``L_CORRIDOR`` or ``Z_CORRIDOR``.
                Currently on ``ONE_CORRIDOR`` is supported. *Default
                ONE_CORRIDOR*.
    """
    if top_left == None:
        top_left = random.choice(ROOM_WIDTH_LIST)
    if top_right == None:
        top_right = random.choice(ROOM_WIDTH_LIST)
    if bottom_left == None:
        bottom_left = random.choice(ROOM_WIDTH_LIST)
    if bottom_right == None:
        bottom_right = random.choice(ROOM_WIDTH_LIST)

    # tl_corr = True
    # tr_corr = True
    # bl_corr = True
    # br_corr = True
    print "tl: %s, tr: %s, bl: %s, br: %s" % (top_left, top_right, bottom_left, bottom_right)
    print "tl: %s, tr: %s, bl: %s, br: %s" % (tl_corr, tr_corr, bl_corr, br_corr)
    # Top row of rooms
    row1 = []
    # Corridor, then bottom row of rooms
    row2 = []

    max_length  = 6*12
    # manor_width = random.randint(max_length/2, max_length)

    # first rooms on either row
    height1 = 7
    height2 = 7
    check_overlap = False
    if top_left < bottom_left or top_left == bottom_left and coinflip():
        height1 += 2
    else:
        height2 += 2
        check_overlap = True

    first = room.Room(width=top_left, height=height1)
    row1.append(first)
    first = room.Room(width=bottom_left, height=height2)
    row2.append(first)
    print "height1: %s, height2: %s" % (height1, height2)

    length1 = top_left + top_right - 2
    if tl_corr:
        length1 += 2
    if tr_corr:
        length1 += 2
    length2 = bottom_left + bottom_right - 2
    if bl_corr:
        length2 += 2
    if br_corr:
        length2 += 2
    print "Row 1:"
    print "room 1: w=%s, length1: %s" % (top_left, length1)
    while len(row1) <= 5:
        # If we have four rooms, one in three chance of not adding any more
        # rooms.
        if len(row1) > 3 and one_chance_in(3):
            break

        new_room = room.Room(width=random.choice(ROOM_WIDTH_LIST))
        row1.append(new_room)
        length1 += new_room.width - 1
        print "room %s: w=%s, length1: %s" % (len(row1), new_room.width, length1)
    print "room %s: w=%s" % (len(row1)+1, top_right)

    manor_width = length1

    print "\nRow 2:"
    print "room 1: w=%s, length2: %s" % (bottom_left, length2)
    while length2 < manor_width:
        dist_left = manor_width - length2 + 1
        if dist_left < 14:
            new_width = dist_left
        else:
            new_width  = random.choice(ROOM_WIDTH_LIST)
            next_width = dist_left - new_width
            if next_width < 7:
                new_width = random.choice((6,7,8))
        new_room = room.Room(width=new_width)
        row2.append(new_room)
        length2 += new_width - 1
        print "room %s: w=%s, length2: %s" % (len(row2), new_width, length2)
    print "room %s: w=%s" % (len(row2)+1, bottom_right)

    # last rooms on either row
    height1 = 7
    height2 = 7
    if top_right < bottom_right or top_right == bottom_right and coinflip():
        height1 += 2
        check_overlap = False
    else:
        height2 += 2
        # check_overlap = True
    print "height1: %s, height2: %s" % (height1, height2)

    first = room.Room(width=top_right, height=height1)
    row1.append(first)
    first = room.Room(width=bottom_right, height=height2)
    row2.append(first)
    print "\nrow1: %s rooms, row2: %s rooms, manor width: %s" % (len(row1), len(row2), manor_width)

    # Now, start drawing it! YAY!

    # First row
    row1_collection = join_row_rooms(row1, tl_corr, tr_corr)

    # second row
    row2_collection = join_row_rooms(row2, bl_corr, br_corr, True)

    # Finally, make a corridor!
    overlap = 3
    if check_overlap:
        overlap = 1
    my_collection = shape.underneath(row1_collection, row2_collection, overlap=overlap, collect=True)
    m = BuilderCollection(my_collection)

    noncorr_left  = min(top_left, bottom_left)
    noncorr_right = min(top_right, bottom_right)
    corridor_length = my_collection.width() - noncorr_left - noncorr_right
    print "noncorr_left: %s, noncorr_right: %s, corridor_length: %s" % (noncorr_left, noncorr_right, corridor_length)
    corridor = MainCorridor(shape.Row(width=corridor_length, fill="."))

    m.append(collection.ShapeCoord(corridor, coord.Coord(noncorr_left, room.Room().height)))

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

def attach_leg (base, leg, side=SIDE_LEFT, placement=PLACE_TOP, x_offset = None):
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

    # Find the corridor's end point
    stop   = coord.Coord(start)
    stop.x = corridor.width()

    if side == SIDE_RIGHT:
        offs = leg[0].width() - start.x
        leg.offset(coord.Coord(stop.x-offs-1, 0))
        if x_offset == None:
            x_offset = stop.x + start.x
    elif side == SIDE_LEFT and x_offset == None:
        x_offset = start.x
    print "vert_offset: %s, x_offset: %s, no_vert_offset: %s" % (vert_offset, x_offset, no_vert_offset)

    new_corridor = Corridor(shape.Column(height=leg.height() + room.Room().height, fill="."))

    corridor_offset = None

    if placement == PLACE_BOTTOM:
        if no_vert_offset:
            base.place_on(leg, offset=coord.Coord(0, vert_offset))
        else:
            left_offset = 0
            if side == SIDE_RIGHT:
                left_offset = base.width()-leg.width()
            base = shape.underneath(base, leg, left_offset=left_offset, overlap=1, collect=True)
        new_corridor[coord.Coord(0, new_corridor.height()-1)] = "#"
        corridor_offset = coord.Coord(x_offset, vert_offset - room.Room().height)
        base.append(new_corridor, corridor_offset)
    elif placement == PLACE_TOP:
        if no_vert_offset:
            base.place_on(leg)
        else:
            left_offset = 0
            if side == SIDE_RIGHT:
                left_offset = leg.width()-base.width()
                print "leg width (%s) - base width (%s) = left_offset (%s)" % (leg.width(), base.width(), left_offset)
            base = shape.underneath(leg, base, left_offset=left_offset, overlap=1, collect=True)
        new_corridor[POS_ORIGIN] = "#"
        corridor_offset = coord.Coord(x_offset, 0)
        base.append(new_corridor, corridor_offset)

    if placement == PLACE_TOP:
        start = coord.Coord(corridor_offset.x - 1, leg.height() - 1)
    elif placement == PLACE_BOTTOM:
        start = coord.Coord(corridor_offset.x - 1, vert_offset - room.Room().height + 1)

    new_shape = shape.Shape(width=3, height=room.Room().height, fill="#")
    new_shape.draw_on(shape.Shape(width=1, height=room.Room().height, fill="."), offset=DIR_EAST, check_conflict=False)

    base = BuilderCollection(base)

    base.draw_on(new_shape, start)
    base.mark_leg(Leg(side, placement, leg=old_leg))

    return base

def build_leg (rooms_tall=2, rooms_wide=2, width_left=12, width_right=12, make_corridor=True, do_cleanup=True):
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

    if width_left == None:
        width_left = random.choice(ROOM_WIDTH_LIST)
    if width_right == None:
        width_right = random.choice(ROOM_WIDTH_LIST)

    for row in xrange(rooms_tall):
        this_row = collection.ShapeCollection()

        left_room = room.Room(width=width_left).as_shape()
        this_row  = shape.adjoin(this_row, left_room, overlap=-1, collect=True)

        if rooms_wide > 1:
            right_room = room.Room(width=width_right).as_shape()
            this_row   = shape.adjoin(this_row, right_room, overlap=-1, collect=True)

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
    side = random.choice([SIDE_LEFT, SIDE_RIGHT])
    placement = random.choice([PLACE_TOP, PLACE_BOTTOM])

    tlc = (side == SIDE_LEFT and placement == PLACE_TOP)
    trc = (side == SIDE_RIGHT and placement == PLACE_TOP)
    blc = (side == SIDE_LEFT and placement == PLACE_BOTTOM)
    brc = (side == SIDE_RIGHT and placement == PLACE_BOTTOM)
    if tlc or blc: # left side
        tlw = random.choice(ROOM_WIDTH_LIST)
        blw = random.choice(ROOM_WIDTH_LIST)
        trw = None
        brw = None
        if tlc:
            if blw < tlw:
                blw = tlw
            left = tlw
        else:
            if tlw < blw:
                tlw = blw
            left = blw
        right = None
    else: # right side
        tlw = None
        blw = None
        trw = random.choice(ROOM_WIDTH_LIST)
        brw = random.choice(ROOM_WIDTH_LIST)
        if trc:
            if brw < trw:
                brw = trw
            right = trw
        else:
            if trw < brw:
                trw = brw
            right = brw
        left = None

    if base is None:
        base = base_builder(top_left=tlw, top_right=trw, bottom_left=blw, bottom_right=brw, tl_corr=tlc, tr_corr=trc, bl_corr=blc, br_corr=brc)

    # Draw the new rooms.
    new_rooms = build_leg(rooms, rooms_wide, width_left=left, width_right=right)

    offset = None
    if side == SIDE_RIGHT:
        offset = base.width() - right - 1
    base = attach_leg(base, new_rooms, side=side, placement=placement, x_offset=offset)
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

    outer = random.choice(ROOM_WIDTH_LIST) # outer leg
    inner = random.choice(ROOM_WIDTH_LIST) # inner leg

    if base is None:
        base = base_builder(top_left=outer, top_right=outer, bottom_left=outer, bottom_right=outer, 
        tl_corr=True, tr_corr=True, bl_corr=True, br_corr=True)

    base = build_U(base, placement=PLACE_TOP, outer=outer, inner=inner)
    base = build_U(base, placement=PLACE_BOTTOM, outer=outer, inner=inner)

    return base

def build_O (base=None):
    if base is None:
        base = base_builder()
    return base

def build_U (base=None, rooms=2, rooms_wide=2, placement=None, outer=None, inner=None):
    # Draw the new rooms.
    if placement is None:
        placement = random.choice([PLACE_TOP, PLACE_BOTTOM])

    if outer == None:
        outer = random.choice(ROOM_WIDTH_LIST) # outer leg
    if inner == None:
        inner = random.choice(ROOM_WIDTH_LIST) # inner leg

    if base is None:
        tlc = (placement == PLACE_TOP)
        trc = tlc
        blc = not tlc
        brc = blc

        noleg = random.choice(ROOM_WIDTH_LIST) # opposite side
        if noleg < outer:
            noleg = outer

        if tlc: # top
            tlw = outer
            trw = outer
            blw = noleg
            brw = noleg
        else: # bottom
            tlw = noleg
            trw = noleg
            blw = outer
            brw = outer

        base = base_builder(top_left=tlw, top_right=trw, bottom_left=blw, bottom_right=brw, tl_corr=tlc, tr_corr=trc, bl_corr=blc, br_corr=brc)

    new_rooms_L = build_leg(rooms, rooms_wide, width_left=outer, width_right=inner)
    new_rooms_R = build_leg(rooms, rooms_wide, width_left=inner, width_right=outer)

    base = attach_leg(base, new_rooms_L, side=SIDE_LEFT, placement=placement)
    base = attach_leg(base, new_rooms_R, side=SIDE_RIGHT, placement=placement, x_offset=base.width() - outer - 1)
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
