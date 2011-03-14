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

import random, builder, room
from interface.features import *
from library.coord import *
from library.random_util import *
from library.feature import *

class ManorCollection (builder.BuilderCollection):
    def __init__ (self, c=[]):
        builder.BuilderCollection.__init__(self, c)

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

    def add_features (self):
        # Translate rooms and corridors into wall and floor features.
        self.init_features()
        # Add doors along corridors.
        self.add_doors()
        # Add windows.
        self.add_windows()
        # Add doors to rooms still missing them.
        self.add_missing_doors()

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
            corrs = self.get_corridor_indices(rand_coord - offset)
            if len(corrs) > 0:
                self.room_props[old_room].add_adjoining_room(corrs[0])
                self.room_props[corrs[0]].add_adjoining_room(old_room)
            else:
                print "no corridor matching doorpos %s of room %s" % (rand_coord, old_room)

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
        """
        for r in self.rooms:
            curr  = self.get_room(r)
            start = curr.pos()
            stop  = start + curr.size()
            print "Room %s: %s" % (r, curr)

            # left-side vertical windows
            if start.x == 0:
                self.add_window(coord.Coord(start.x, start.y + 2), coord.Coord(start.x, stop.y - 3))
                self.room_props[r].add_window(DIR_WEST)
            elif (self.get_feature(coord.Coord(start.x-1, start.y+1)) == NOTHING
            or self.get_feature(coord.Coord(start.x-1, stop.y-1)) == NOTHING):
                self.add_window(coord.Coord(start.x, start.y + 2), coord.Coord(start.x, stop.y - 3), DIR_WEST)
                self.room_props[r].add_window(DIR_WEST)

            # right-side vertical windows
            if stop.x == self.size().x:
                self.add_window(coord.Coord(stop.x - 1, start.y + 2), coord.Coord(stop.x - 1, stop.y - 3))
                self.room_props[r].add_window(DIR_EAST)
            elif (self.get_feature(coord.Coord(stop.x+1, start.y+1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x+1, stop.y-1)) == NOTHING):
                self.add_window(coord.Coord(stop.x - 1, start.y + 2), coord.Coord(stop.x - 1, stop.y - 3), DIR_EAST)
                self.room_props[r].add_window(DIR_EAST)

            # top horizontal windows
            if start.y == 0:
                self.add_window(coord.Coord(start.x + 2, start.y), coord.Coord(stop.x - 3, start.y))
                self.room_props[r].add_window(DIR_NORTH)
            elif (self.get_feature(coord.Coord(start.x+1, start.y-1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x-1, start.y-1)) == NOTHING):
                self.add_window(coord.Coord(start.x + 2, start.y), coord.Coord(stop.x - 3, start.y), DIR_NORTH)
                self.room_props[r].add_window(DIR_NORTH)

            # bottom horizontal windows
            if stop.y == self.size().y:
                self.add_window(coord.Coord(start.x + 2, stop.y - 1), coord.Coord(stop.x - 3, stop.y - 1))
                self.room_props[r].add_window(DIR_SOUTH)
            elif (self.get_feature(coord.Coord(start.x+1, stop.y+1)) == NOTHING
            or self.get_feature(coord.Coord(stop.x-1, stop.y+1)) == NOTHING):
                self.add_window(coord.Coord(start.x + 2, stop.y - 1), coord.Coord(stop.x - 3, stop.y - 1), DIR_SOUTH)
                self.room_props[r].add_window(DIR_SOUTH)

    def add_missing_doors (self):
        """
        Add doors to rooms that still lack them.
        """
        door_rooms = []
        for d in self.doors:
            rooms = self.get_room_index(d, False)
            if len(rooms) > 0:
                for r in rooms:
                    if r not in door_rooms:
                        door_rooms.append(r)

        rooms = self.rooms[:]
        random.shuffle(rooms)
        for r in rooms:
            if r in door_rooms:
                continue

            curr  = self.get_room(r)
            start = curr.pos()
            stop  = start + curr.size()
            print "Room %s: %s" % (r, curr)

            door_candidates = []
            rp = self.room_props[r]
            door_dirs = [DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST]
            for windir in rp.windows:
                door_dirs.remove(windir)

            for dd in door_dirs:
                if dd == DIR_WEST:
                    dpos = self.pick_door_along_wall(coord.Coord(start.x, start.y + 1), coord.Coord(start.x, stop.y - 2), DIR_WEST)
                elif dd == DIR_EAST:
                    dpos = self.pick_door_along_wall(coord.Coord(stop.x - 1, start.y + 1), coord.Coord(stop.x - 1, stop.y - 2), DIR_EAST)
                elif dd == DIR_NORTH:
                    dpos = self.pick_door_along_wall(coord.Coord(start.x + 1, start.y), coord.Coord(stop.x - 2, start.y), DIR_NORTH)
                elif dd == DIR_SOUTH:
                    dpos = self.pick_door_along_wall(coord.Coord(start.x + 1, stop.y - 1), coord.Coord(stop.x - 2, stop.y - 1), DIR_SOUTH)
                door_candidates.append(dpos)

            # Adding doors to all applicable walls guarantees that
            # all rooms are fully connected, but does mean that some
            # rooms get 2-3 doors.
            for d in door_candidates:
                print "==> add door at pos %s" % d
                self.features.__setitem__(d, OPEN_DOOR)
                self.doors.append(d)

                # Update door-less rooms.
                other_rooms = self.get_room_indices(d)
                for r in other_rooms:
                    if r not in door_rooms:
                        door_rooms.append(r)

    def init_room_names (self, list = None):
        owner_list = []
        if list != None:
            owner_list = list

        # There should be at least 7 rooms available to the public.
        # This is only really a problem for smallish layouts, if there
        # are many suspects. (jpeg)
        max_no_bedrooms = len(self.rooms) - 7
        print "-------\nallow for max. %s bedrooms" % max_no_bedrooms

        corrs = self.corridors[:]
        if len(corrs) > 1:
            corrs.remove(self.main_corridor)
            random.shuffle(corrs)
            utility = True
            for c in corrs:
                section = "domestic"
                if utility:
                    section = "utility"
                elif len(owner_list) > 0:
                    section = "bedrooms"
                print "-------\nCorridor %s is marked as %s" % (c, section)
                corrprop = self.room_props[c]
                for r in corrprop.adj_rooms:
                    if r in self.corridors:
                        continue

                    rp = self.room_props[r]
                    if rp.has_data:
                        continue

                    if (not utility and len(owner_list) > 0
                    and rp.is_good_bedroom()):
                        owner = owner_list[0]
                        owner_list.remove(owner)
                        rp.make_bedroom(owner)
                        max_no_bedrooms -= 1
                        continue

                    rp.fill_from_database(utility)

                utility = False

        # One of the rooms off the main corridor is the entrance hall.
        c = self.main_corridor
        corrprop = self.room_props[c]
        e_hall_candidates = []
        for r in corrprop.adj_rooms:
            if r in self.corridors:
                continue

            rp = self.room_props[r]
            if rp.has_data or len(rp.windows) == 0:
                continue
            e_hall_candidates.append(r)

        if len(e_hall_candidates) == 0:
            print "-------\nNo entrance hall for this manor!"
        else:
            self.entrance_hall = random.choice(e_hall_candidates)
            rp = self.room_props[self.entrance_hall]
            rp.name = "entrance hall"
            rp.has_data = True
            max_no_bedrooms -= 1
            print "-------\nentrance hall: room %s" % self.entrance_hall

        if len(owner_list) > 0:
            print "-------\nremaining rooms - allow for max. %s bedrooms" % max_no_bedrooms
            rooms = self.rooms[:]
            random.shuffle(rooms)
            for r in rooms:
                rp = self.room_props[r]
                if rp.has_data:
                    continue

                if (len(owner_list) > 0 and max_no_bedrooms > 0
                and rp.is_good_bedroom()):
                    owner = owner_list[0]
                    owner_list.remove(owner)
                    rp.make_bedroom(owner)
                    max_no_bedrooms -= 1

        print "-------\nassign remaining rooms"
        rooms = self.rooms[:]
        random.shuffle(rooms)
        for r in rooms:
            rp = self.room_props[r]
            if rp.has_data:
                continue

            if (len(owner_list) > 0 and max_no_bedrooms > 0
            and len(rp.adj_rooms) == 1):
                owner = owner_list[0]
                owner_list.remove(owner)
                rp.make_bedroom(owner)
                max_no_bedrooms -= 1
                continue

            rp.fill_from_database()

        self.update_adjoining_rooms()

    def update_adjoining_rooms (self):
        for r in self.get_room_corridors():
            rp = self.room_props[r]
            for adjr in rp.adj_rooms:
                rp2  = self.room_props[adjr]
                name = rp2.name
                rp.add_adjoining_room_name(name)

    def get_bedroom_id (self, owner, rids = None, do_chance = True):
        if do_chance and not one_chance_in(4):
            return -1

        if rids == None:
            rids = self.rooms
        rp = self.room_props
        for r in rids:
            if owner in rp[r].owners:
                return r
        return -1

    def pick_random_public_room (self, rids = None, force_adj_corr = False):
        if rids == None:
            rids = self.rooms
        rp = self.room_props
        candidates = []
        for r in rids:
            if force_adj_corr:
                found_corr = False
                for adj in rp[r].adj_rooms:
                    if rp[adj].is_corridor:
                        found_corr = True
                        break
                if not found_corr:
                    continue

            if len(rp[r].owners) == 0:
                candidates.append(r)
        if len(candidates) == 0:
            return -1
        return random.choice(candidates)

    def pick_room_for_suspect (self, rids, idx1, idx2 = None, force_adj_corr = False):
        rp = self.room_props
        r = self.get_bedroom_id(idx1, rids)
        if r != -1:
            return r

        if idx2 != None:
            r = self.get_bedroom_id(idx2, rids)
            if r != -1:
                return r

        r = self.pick_random_public_room(rids, force_adj_corr)
        if r != -1:
            return r

        # Try for bedrooms again.
        r = self.get_bedroom_id(idx1, rids)
        if r != -1:
            return r

        if idx2 != None:
            r = self.get_bedroom_id(idx2, rids)

        return r
