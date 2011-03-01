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

import random, copy, room
from interface.features import *
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
    manor = ManorCollection(my_collection)

    corridor_length = my_collection.width() - room_width * 2
    corridor = MainCorridor(shape.Row(width=corridor_length, fill="."))

    manor.append(collection.ShapeCoord(corridor, coord.Coord(room_width, room_height)))

    return manor

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

class ManorCollection (collection.ShapeCollection):
    corridors = None
    rooms     = None
    legs      = None
    main_corridor = None

    def __init__ (self, c=[]):
        if c != [] and isinstance(c, ManorCollection):
            self.legs = c.legs

        collection.ShapeCollection.__init__(self, c)
        self.rebuild()

    def copy (self):
        my_copy = ManorCollection(copy.copy(self._shapes))
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

    def print_corridors (self):
        """
        Debugging method. Iterates over all corridors and prints the location
        and size of each corridor within the manor.
        """
        for idx in self.corridors:
            print "Corridor %s: %s" % (idx, self.corridor(idx))

    def get_corridor_index (self, pos, single = True):
        """
        Returns the index of the corridor a coordinate belongs to, or None
        if it doesn't lie in any corridor.
        If it's part of the overlap region, the first index is returned.

        :``pos``: A coord. *Required*
        :``single``: If true, returns the first index encountered.
                     Otherwise, a list containing all matching indices. *Default true*.
        """
        list = []
        for idx in self.corridors:
            corr = self.corridor(idx)
            r = corr.size()
            c = corr.pos()
            if (pos.x >= c.x and pos.x <= c.x + r.x
                and pos.y >= c.y and pos.y <= c.y + r.y):
                if single:
                    return idx
                list.append(idx)
        if single:
            return None
        return list

    def get_corridor_indices (self, pos):
        """
        Returns a list of indices of all corridors a coordinate belongs to,
        or None if it's outside the manor.

        :``pos``: A coord. *Required*
        """
        return self.get_corridor_index(pos, False)

    def get_room (self, index):
        assert index in self.rooms
        return self[index]

    def get_rooms (self):
        if not self.rooms:
            return None
        return self.rooms

    def print_rooms (self):
        """
        Debugging method. Iterates over all rooms and prints the location
        and size of each room within the manor.
        """
        for idx in self.rooms:
            print "Room %s: %s" % (idx, self.get_room(idx))

    def get_room_index (self, pos, single = True):
        """
        Returns the index of the room a coordinate belongs to, or None if
        it's outside the manor.
        If it's part of the overlap region, the first index is returned.

        :``pos``: A coord. *Required*
        :``single``: If true, returns the first index encountered.
                     Otherwise, a list containing all matching indices. *Default true*.
        """
        list = []
        for idx in self.rooms:
            curr = self.get_room(idx)
            r = curr.size()
            c = curr.pos()
            if (pos.x >= c.x and pos.x <= c.x + r.x
                and pos.y >= c.y and pos.y <= c.y + r.y):
                if single:
                    return idx
                list.append(idx)
        if single:
            return None
        return list

    def get_room_indices (self, pos):
        """
        Returns a list of indices of all rooms a coordinate belongs to,
        or None if it's outside the manor.

        :``pos``: A coord. *Required*.
        """
        return self.get_room_index(pos, False)

    def get_room_corridor_indices (self, pos):
        """
        Returns a list of indices of all rooms and corridors a coordinate belongs to,
        or None if it's outside the manor.

        :``pos``: A coord. *Required*.
        """
        rooms = self.get_room_index(pos, False)
        corrs = self.get_corridor_index(pos, False)
        for c in corrs:
            rooms.append(c)
        return rooms

    def get_room_corridors (self):
        """
        Get a combined list including both room and corridor indices.
        """
        # I might be overly cautious here, but it's so easy to overwrite
        # existing lists by setting references without meaning to. (jpeg)
        room_corridors = []
        for r in self.rooms:
            room_corridors.append(r)
        for c in self.corridors:
            room_corridors.append(c)
        room_corridors.sort()
        return room_corridors

    def get_corridor_name (self, idx):
        assert(idx in self.corridors)
        if idx == self.main_corridor:
            return "main corridor"

        corr  = self.corridor(idx)
        start = corr.pos()
        stop  = start + coord.Coord(corr.width(), corr.height())

        dir_horizontal = ""
        if start.y < self.size().y/4:
            dir_horizontal += "north"
        elif stop.y > 3*self.size().y/4:
            dir_horizontal += "south"
        dir_vertical = ""
        if start.x < self.size().x/4:
            dir_vertical += "west"
        elif stop.x > 3*self.size().x/4:
            dir_vertical += "east"

        # only one other corridor
        if len(self.corridors) == 2:
            if dir_horizontal != "" and dir_vertical != "":
                if coinflip():
                    dir_horizontal = ""
                else:
                    dir_vertical = ""
        # two other corridors
        elif len(self.corridors) == 3:
            if corr.width() == 1: # vertical
                dir_horizontal = ""
            else:
                dir_vertical = ""

        # else just combine both values
        if dir_horizontal != "" or dir_vertical != "":
            return "%s%s corridor" % (dir_horizontal, dir_vertical)

        # If none of these match, just return the number.
        return "corridor %s" % idx

    def init_room_properties (self):
        """
        Initialises a list of RoomProp objects for each room and corridor
        in the manor.
        """
        self.room_props = []
        for r in self.get_room_corridors():
            if r in self.rooms:
                curr   = self.get_room(r)
                start  = curr.pos()
                size   = curr.size()
                width  = size.x
                height = size.y
                room_prop = room.RoomProps("room %s" % r, start, width, height)
            else:
                corr   = self.corridor(r)
                start  = corr.pos()
                width  = corr.width()
                height = corr.height()
                name   = self.get_corridor_name(r)

                room_prop = room.RoomProps(name, start, width, height)
                room_prop.mark_as_corridor()

            self.room_props.append(room_prop)

    def get_roomprop (self, idx):
        """
        Returns a RoomProp object for a given room index.

        :``idx``: A room or corridor index. *Required*.
        """
        if not self.room_props:
            return None
        assert(idx < len(self.room_props))
        return self.room_props[idx]

    def init_features (self):
        """
        Initialise the manor's feature grid, placing floor and walls as
        defined by the rooms/corridor layout.
        """
        self.init_room_properties()
        self.features = FeatureGrid(self.size().x, self.size().y)

        print "Manor size: %s" % self.size()
        print "Feature size: %s" % self.features.size()

        # Iterate over all rooms and corridors, and mark positions within
        # them as floor, and their boundaries as walls.
        for r in self.get_room_corridors():
            is_corridor = False # The "room" is actually a corridor.
            if r in self.rooms:
                curr = self.get_room(r)
            else:
                is_corridor = True
                curr = self.corridor(r)

            start = curr.pos()
            stop  = curr.pos() + curr.size()
            # Note: Currently, only the main corridor is ever horizontal
            # but that might change in the future.
            horizontal = False # If a corridor, it's a horizontal one.

            # Debugging output, and setting horizontal.
            if is_corridor:
                if curr.height() == 1:
                    horizontal = True
                    direction = "horizontal"
                else:
                    direction = "vertical"
                # print "Corridor %s: start=%s, stop=%s (%s)" % (r, start, stop, direction)

            # Iterate over all coordinates within the room.
            for pos in coord.RectangleIterator(start, stop):
                # If we've reached the manor boundary, this is a wall.
                if (pos.x == 0 or pos.x == self.size().x -1
                    or pos.y == 0 or pos.y == self.size().y - 1):
                    self.features.__setitem__(pos, WALL)
                # Corridors overwrite walls previously set by rooms.
                elif is_corridor:
                    self.features.__setitem__(pos, FLOOR)
                    # print pos
                    # Depending on the corridor orientation, mark the
                    # adjacent non-corridor squares as walls.
                    adjacent = []
                    if horizontal:
                        adjacent = (DIR_NORTH, DIR_SOUTH)
                    else:
                        adjacent = (DIR_WEST, DIR_EAST)
                    for dir in adjacent:
                        pos2 = pos + dir
                        # self.features.__setitem__(pos2, WALL)
                        if pos2 <= 0 or pos2 >= self.size():
                            continue
                        corridx = self.get_corridor_indices(pos2)
                        # print "pos2: %s -> corridors=%s" % (pos2, corridx),
                        if r in corridx:
                            corridx.remove(r)
                            # print corridx
                        # else:
                            # print
                        if len(corridx) == 0:
                            self.features.__setitem__(pos2, WALL)
                # The room boundary is always a wall.
                elif (pos.x == start.x or pos.x == stop.x - 1
                    or pos.y == start.y or pos.y == stop.y - 1):
                    self.features.__setitem__(pos, WALL)
                # Otherwise, we are inside the room.
                # Mark as floor but don't overwrite previously placed walls.
                elif self.get_feature(pos) != WALL:
                    self.features.__setitem__(pos, FLOOR)

    def get_feature (self, pos):
        """
        Returns the feature for the given position.

        :``pos``: A coordinate within the manor. *Required*
        """
        if pos < DIR_NOWHERE or pos >= self.size():
            print "Invalid coord %s in manor of size %s" % (pos, self.size())
            return NOTHING

        return self.features.__getitem__(pos)

    def add_doors_along_corridor (self, start, stop, offset = DIR_NOWHERE):
        """
        Walks along a corridor, and for each adjacent room picks a random
        wall spot to turn into a door.

        :``start``: The corridor's starting position. *Required*
        :``stop``: The corridor's end position. *Required*.
        :``offset``: A coordinate specifying how the door position needs to be shifted. *Default (0,0)*.
        """
        print "add_doors_along_corridor(start=%s, stop=%s, offset=%s)" % (start, stop, offset)
        assert stop > start

        candidates = [] # All valid door spots for the current room.
        old_room   = -1 # The index of the most recent room seen.

        for pos in coord.RectangleIterator(start, stop + 1):
            if (pos.x + offset.x < 2 or pos.x + offset.x >= self.size().x - 1
            or pos.y + offset.y < 2 or pos.y + offset.y >= self.size().y - 1):
                continue

            if self.get_feature(pos + offset) != WALL:
                continue
            rooms = self.get_room_indices(pos)
            corrs = self.get_corridor_indices(pos)
            # Make sure there's only exactly room for this wall.
            # There also may be no other corridor except this one.
            if len(rooms) == 1 and len(corrs) == 1:
                # print "(%s, %s) -> %s" % (pos.x, pos.y, rooms)
                curr_room = rooms[0]
                if old_room != curr_room:
                    # We've reached another room. Time to pick a door spot for the old room.
                    if len(candidates):
                        rand_coord = random.choice(candidates) + offset
                        print "==> pick %s" % rand_coord
                        self.features.__setitem__(rand_coord, CLOSED_DOOR)
                        self.room_props[old_room].add_adjoining_room(corrs[0])
                        self.room_props[corrs[0]].add_adjoining_room(old_room)
                        self.doors.append(rand_coord)
                        candidates = []
                    # print "curr. room: %s" % curr_room
                old_room = curr_room
                candidates.append(pos)

        # The corridor has reached an end. Pick a door spot for the last room seen.
        if len(candidates):
            rand_coord = random.choice(candidates) + offset
            print "==> pick %s" % rand_coord
            self.features.__setitem__(rand_coord, CLOSED_DOOR)
            self.doors.append(rand_coord)
            corrs = self.get_corridor_indices(start)
            self.room_props[old_room].add_adjoining_room(corrs[0])
            self.room_props[corrs[0]].add_adjoining_room(old_room)

    def init_room_names (self):
        corrs = self.corridors[:]
        if len(corrs) > 1:
            corrs.remove(self.main_corridor)
            random.shuffle(corrs)
            utility = True
            for c in corrs:
                section = "domestic"
                if utility:
                    section = "utility"
                print "-------\nCorridor %s is marked as %s" % (c, section)
                corrprop = self.room_props[c]
                for r in corrprop.adj_rooms:
                    if r in self.corridors:
                        continue

                    rp = self.room_props[r]
                    if not rp.db_data:
                        rp.fill_from_database(utility)
                utility = False

        c = self.main_corridor
        corrprop = self.room_props[c]
        e_hall_candidates = []
        for r in corrprop.adj_rooms:
            if r in self.corridors:
                continue

            rp = self.room_props[r]
            if rp.db_data or len(rp.windows) == 0:
                continue
            e_hall_candidates.append(r)

        if len(e_hall_candidates) == 0:
            print "-------\nNo entrance hall for this manor!"
        else:
            self.entrance_hall = random.choice(e_hall_candidates)
            rp = self.room_props[self.entrance_hall]
            rp.name = "entrance hall"
            print "-------\nentrance hall: room %s" % self.entrance_hall

        print "-------\nassign remaining rooms"
        for r in self.rooms:
            if r == self.entrance_hall:
                continue

            rp = self.room_props[r]
            if rp.db_data:
                continue

            rp.fill_from_database()

    def update_adjoining_rooms (self):
        self.init_room_names()
        for r in self.get_room_corridors():
            rp = self.room_props[r]
            for adjr in rp.adj_rooms:
                rp2  = self.room_props[adjr]
                name = rp2.name
                rp.add_adjoining_room_name(name)

    def add_doors (self):
        """
        For each corridor, adds doors to adjacent rooms.
        """
        # print "Adding doors..."
        self.doors = []
        corr = self.corridors
        for c in corr:
            candidates = []
            w   = self.corridor(c).width()
            h   = self.corridor(c).height()
            pos = self.corridor(c).pos()
            print "Corridor %s: %s" % (c, self.corridor(c))
            # Depending on the corridor's orientation, check the parallel runs
            # to the left and right, or above and below the corridor.
            # Walls to the left and top of a corridor position are not
            # considered part of the corridor, so we need to use a shim
            # to add doors on those sides as well.
            if w > 1: # vertical corridor
                self.add_doors_along_corridor(coord.Coord(pos.x, pos.y), coord.Coord(pos.x + w, pos.y), DIR_NORTH)
                self.add_doors_along_corridor(coord.Coord(pos.x, pos.y + h), coord.Coord(pos.x + w, pos.y + h))
            else: # horizontal corridor
                self.add_doors_along_corridor(coord.Coord(pos.x, pos.y), coord.Coord(pos.x, pos.y + h), DIR_WEST)
                self.add_doors_along_corridor(coord.Coord(pos.x + w, pos.y), coord.Coord(pos.x + w, pos.y + h))

    def pick_door_along_wall (self, start, stop, offset):
        """
        Picks a door spot for a wall specified by two coordinates.

        :``start``: The wall's starting position. *Required*
        :``stop``: The wall's end position. *Required*.
        :``offset_check``: A Coord offset to check for adjacent non-walls. *Required*.
        """
        candidates = []
        for pos in coord.RectangleIterator(start, stop + 1):
            if (self.get_feature(pos) == WALL
            and self.get_feature(pos + offset) != WALL):
                candidates.append(pos)

        assert(len(candidates) > 0)
        door_pos = random.choice(candidates)
        rooms = self.get_room_corridor_indices(door_pos)
        for i1 in xrange(len(rooms)):
            r1 = rooms[i1]
            for i2 in xrange(i1+1, len(rooms)):
                r2 = rooms[i2]
                rp1 = self.room_props[r1]
                rp2 = self.room_props[r2]
                rp1.add_adjoining_room(r2)
                rp2.add_adjoining_room(r1)

        return door_pos

    def add_window (self, start, stop, offset_check = DIR_NOWHERE):
        """
        Adds windows to the wall specified by two coordinates.

        :``start``: The wall's starting position. *Required*
        :``stop``: The wall's end position. *Required*.
        :``offset_check``: A Coord offset to check for empty space. *Default (0,0)*.
        """
        if start.x == stop.x:
            window = WINDOW_V
        elif start.y == stop.y:
            window = WINDOW_H
        else:
            return

        # If we got an offset passed in, we need to check whether adjacent
        # positions are really empty, so the window doesn't look out on
        # a wall or something.
        # NOTE: Naturally, should we decide to fill the nothingness with
        #       a garden of some sort, the whole routine will have to be
        #       changed. (jpeg)
        if offset_check != DIR_NOWHERE:
            # print "offset: %s, start=%s, stop=%s" % (offset_check, start, stop)
            seen_nothing = False
            for pos in coord.RectangleIterator(start, stop + 1):
                adj_pos = pos + offset_check
                if self.get_feature(adj_pos) == NOTHING:
                    seen_nothing = True
                else:
                    if seen_nothing: # start already handled
                        if window == WINDOW_H:
                            stop.x = pos.x - 1
                        else:
                            stop.y = pos.y - 1
                        break
                    else:
                        if window == WINDOW_H:
                            start.x = pos.x + 1
                        else:
                            start.y = pos.y + 1
            # print "new start=%s, stop=%s" % (start, stop)

        full_window = False
        if start.x == stop.x:
            length = stop.y - start.y + 1
        elif start.y == stop.y:
            length = stop.x - start.x + 1
        # else:
            # return

        # print "draw window for wall of length %s at (%s, %s)" % (length, start, stop)
        if length < 5 or (length < 7 and one_chance_in(3)):
            full_window = True
        elif length >= 6 and one_chance_in(3):
            # For really large windows, make them a bit smaller and
            # move them into the centre.
            full_window = True
            if window == WINDOW_V:
                start.y += 1
                stop.y  -= 1
            else:
                start.x += 1
                stop.x  -= 1
        else:
            # Split larger windows into two smaller ones.
            midpost = length/2
            width   = 1
            if length == 5:
                midpost += 1
                width = 0
            elif length%2 == 1:
                # midpost -= 1
                width    = 2

        # For full windows, there's a chance of making them smaller
        # and placing them slightly off-center.
        if full_window and one_chance_in(3):
            shift = random.randint(1, max(1,length/3))
            if window == WINDOW_H:
                if coinflip():
                    start.x += shift
                else:
                    stop.x  -= shift
            else:
                if coinflip():
                    start.y += shift
                else:
                    stop.y  -= shift

        count = 0
        for pos in coord.RectangleIterator(start, stop + 1):
            count += 1
            if full_window or count < midpost or count > midpost + width:
                self.features.__setitem__(pos, window)

    def add_windows (self):
        """
        Adds windows to the outer walls of the manor.
        Also adds doors to rooms that still lack them.
        """
        door_rooms = []
        for d in self.doors:
            rooms = self.get_room_index(d, False)
            if len(rooms) > 0:
                for r in rooms:
                    if r not in door_rooms:
                        door_rooms.append(r)

        for r in self.rooms:
            curr  = self.get_room(r)
            start = curr.pos()
            stop  = start + curr.size()
            print "Room %s: %s" % (r, curr)

            needs_door = (r not in door_rooms)
            # if needs_door:
                # print "-> room needs a door!"

            door_candidates = []
            # left-side vertical windows
            if start.x == 0:
                self.add_window(coord.Coord(start.x, start.y + 2), coord.Coord(start.x, stop.y - 3))
                self.room_props[r].add_window(DIR_WEST)
            elif (self.get_feature(coord.Coord(start.x-1, start.y+1)) == NOTHING
            or self.get_feature(coord.Coord(start.x-1, stop.y-1)) == NOTHING):
                self.add_window(coord.Coord(start.x, start.y + 2), coord.Coord(start.x, stop.y - 3), DIR_WEST)
                self.room_props[r].add_window(DIR_WEST)
            elif needs_door: # place a door
                d = self.pick_door_along_wall(coord.Coord(start.x, start.y + 1), coord.Coord(start.x, stop.y - 2), DIR_WEST)
                door_candidates.append(d)

            # right-side vertical windows
            if stop.x == self.size().x:
                self.add_window(coord.Coord(stop.x - 1, start.y + 2), coord.Coord(stop.x - 1, stop.y - 3))
                self.room_props[r].add_window(DIR_EAST)
            elif (self.get_feature(coord.Coord(stop.x+1, start.y+1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x+1, stop.y-1)) == NOTHING):
                self.add_window(coord.Coord(stop.x - 1, start.y + 2), coord.Coord(stop.x - 1, stop.y - 3), DIR_EAST)
                self.room_props[r].add_window(DIR_EAST)
            elif needs_door: # place a door
                d = self.pick_door_along_wall(coord.Coord(stop.x - 1, start.y + 1), coord.Coord(stop.x - 1, stop.y - 2), DIR_EAST)
                door_candidates.append(d)

            # top horizontal windows
            if start.y == 0:
                self.add_window(coord.Coord(start.x + 2, start.y), coord.Coord(stop.x - 3, start.y))
                self.room_props[r].add_window(DIR_NORTH)
            elif (self.get_feature(coord.Coord(start.x+1, start.y-1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x-1, start.y-1)) == NOTHING):
                self.add_window(coord.Coord(start.x + 2, start.y), coord.Coord(stop.x - 3, start.y), DIR_NORTH)
                self.room_props[r].add_window(DIR_NORTH)
            elif needs_door: # place a door
                d = self.pick_door_along_wall(coord.Coord(start.x + 1, start.y), coord.Coord(stop.x - 2, start.y), DIR_NORTH)
                door_candidates.append(d)

            # bottom horizontal windows
            if stop.y == self.size().y:
                self.add_window(coord.Coord(start.x + 2, stop.y - 1), coord.Coord(stop.x - 3, stop.y - 1))
                self.room_props[r].add_window(DIR_SOUTH)
            elif (self.get_feature(coord.Coord(start.x+1, stop.y+1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x-1, stop.y+1)) == NOTHING):
                self.add_window(coord.Coord(start.x + 2, stop.y - 1), coord.Coord(stop.x - 3, stop.y - 1), DIR_SOUTH)
                self.room_props[r].add_window(DIR_SOUTH)
            elif needs_door: # place a door
                d = self.pick_door_along_wall(coord.Coord(start.x + 1, stop.y - 1), coord.Coord(stop.x - 2, stop.y - 1), DIR_SOUTH)
                door_candidates.append(d)

            if needs_door:
                # Adding doors to all applicable walls guarantees that
                # all rooms are fully connected, but does mean that some
                # rooms get 2-3 doors.
                for d in door_candidates:
                    print "==> add door at pos %s" % d
                    self.features.__setitem__(d, OPEN_DOOR)
                    self.doors.append(d)

                    # Update door-less rooms.
                    rooms = self.get_room_indices(d)
                    for r in rooms:
                        if r not in door_rooms:
                            door_rooms.append(r)

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
        wrapper.__doc__ = function.__doc__ + "\n\nCalling this function automatically rebuilds the ManorCollection index."
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

    base = ManorCollection(base)

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
