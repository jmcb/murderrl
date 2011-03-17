#!/usr/bin/env python

import random
from library.coord import *
from library import shape
import database.database as db
from interface.output import *

ROOM_WIDTH  = 12
ROOM_HEIGHT = 7

def join_strings (list):
    if len(list) == 0:
        return ""

    if len(list) == 1:
        return list[0]

    last = list.pop()
    return "%s and %s" % (', '.join(list), last)

class Room (object):
    """
    Currently a builder-only representation of a room.
    """
    def __init__ (self, width=ROOM_WIDTH, height=ROOM_HEIGHT, start=None, stop=None):
        """
        Create a room.

        :``width``: The width of the room. *Default 10*.
        :``height``: The height of the room. *Default 6*.
        :``start``: A coord denoting the top-left point of the room. *Default None*.
        :``stop``: A coord denoting the bottom-right point of the room. *Default None*.

        """
        self.width  = width
        self.height = height
        self.start  = start
        self.stop   = stop

    def as_shape (self):
        """
        Converts the room into a Shape object, by way of a Box.
        """
        return shape.Box(width=self.width, height=self.height, border=1, fill=".", border_fill="#")

    def __repr__ (self):
        return "<Room width=%s,height=%s,name=%s,start=%s,stop=%s>" % (self.width,self.height,self.name,self.start,self.stop)

def check_haswindows_passage (db_room):
    return db_room.is_passage and db_room.has_windows

def check_is_nowindows_passage (db_room):
    return db_room.is_passage and not db_room.has_windows

def check_is_passage (db_room):
    return db_room.is_passage

def check_haswindows (db_room):
    return db_room.has_windows

def check_nowindows (db_room):
    return not db_room.has_windows

def check_is_utility (db_room):
    return db_room.section == "utility"

def check_not_utility (db_room):
    return db_room.section != "utility"

class RoomProps (Room):
    def __init__ (self, name=None, start=None, width=ROOM_WIDTH, height=ROOM_HEIGHT):
        Room.__init__(self, width, height, start)
        self.init_db_props(name, "corridor")

        # Initialise a few variables for later.
        self.is_corridor    = False
        self.adj_rooms      = [] # adjoining room ids (connected by doors)
        self.adj_room_names = [] # names for the above
        self.windows        = [] # on which sides a room has windows
        self.owners         = [] # private room of one or more person(s)
        self.owner_names    = []

    def init_db_props(self, name, section=None, prep="in", complete=False):
        self.name       = name
        self.section    = section
        self.prep       = prep # preposition
        self.has_data   = complete

    def __str__ (self, article=False):
        if not self.name:
            return "buggy crawl space"

        if article and len(self.owners) == 0:
            return "the %s" % self.name

        return self.name

    def mark_as_corridor (self, is_corridor = True):
        self.is_corridor = is_corridor

    def is_a_corridor (self):
        return self.is_corridor

    def add_adjoining_room (self, ridx):
        if not ridx in self.adj_rooms:
            self.adj_rooms.append(ridx)

    def add_adjoining_room_name (self, name):
        self.adj_room_names.append(name)
        assert(len(self.adj_rooms) >= len(self.adj_room_names))

    def add_window (self, dir):
        self.windows.append(dir)

    def is_good_bedroom (self):
        # May not be a passage room, needs windows.
        return len(self.adj_rooms) == 1 and len(self.windows) > 0

    def make_bedroom (self, owner):
        assert(len(owner) > 1)
        owner_id   = owner[0]
        owner_name = owner[1]
        if isinstance(owner_name, list):
            owner_name = join_strings(owner_name)
        room_name  = "%s's bedroom" % owner_name
        print room_name
        self.init_db_props(room_name, "domestic", "in", True)
        if isinstance(owner_id, list):
            self.owners = owner_id
        else:
            self.owners.append(owner_id)
        self.owner_names.append(owner_name)

    def fill_from_database (self, utility = None, owner = None):
        """
        Pull a random room name from the database.
        """
        if owner != None and self.is_good_bedroom():
            self.make_bedroom(owner)
            return

        dbr = db.get_database("rooms")
        new_room = None
        # Section checks override all other checks.
        if utility == True:
            new_room = dbr.random_pop(check_is_utility)
        elif utility == False:
            new_room = dbr.random_pop(check_not_utility)

        if new_room == None and len(self.adj_rooms) > 1:
            if len(self.windows) == 0:
                new_room = dbr.random_pop(check_is_nowindows_passage)
            else:
                new_room = dbr.random_pop(check_haswindows_passage)

            if new_room == None:
                new_room = dbr.random_pop(check_is_passage)

        if new_room == None:
            if len(self.windows) == 0:
                new_room = dbr.random_pop(check_nowindows)
            else:
                new_room = dbr.random_pop(check_haswindows)

            if new_room == None:
                new_room = dbr.random_pop()

        if new_room:
            print new_room.name
            self.init_db_props(new_room.name, new_room.section, new_room.prep, True)

    def describe_window_dirs (self):
        dirs = []
        for d in self.windows:
            if d == DIR_NORTH:
                dirs.append("north")
            elif d == DIR_SOUTH:
                dirs.append("south")
            elif d == DIR_WEST:
                dirs.append("west")
            elif d == DIR_EAST:
                dirs.append("east")
            else:
                dirs.append("invalid direction")

        return join_strings(dirs)

    def describe_windows (self):
        desc = "There "
        if len(self.windows) == 0:
            room_or_corridor = "room"
            if self.is_a_corridor():
                room_or_corridor = "corridor"
            desc += "are no windows in this %s." % room_or_corridor
        else:
            if len(self.windows) == 1:
                desc += "is a window "
            else:
                desc += "are windows "
            desc += "to the %s." % self.describe_window_dirs()

        return desc

    def describe_exits (self):
        if len(self.adj_room_names) == 0:
            return ""

        desc = "There "
        if len(self.adj_rooms) == 1:
            desc += "is a door"
        else:
            desc += "are doors"
        assert(len(self.adj_room_names) > 0)
        desc += " leading to %s." % join_strings(self.adj_room_names)

        return desc

    def get_room_description (self):
        """
        Returns a room's description.
        """
        # Very basic right now, but will eventually include adjoining rooms
        # and furniture.
        article = "the "
        if len(self.owners) > 0:
            article = ""
        desc = "You are standing %s %s%s.\n\n" % (self.prep, article, self.name)
        desc += "It is part of the manor's %s area.\n" % self.section

        desc += "%s\n\n" % self.describe_windows()
        desc += self.describe_exits()

        return desc

    def describe (self):
        """
        Print a room description.
        """
        print_screen(self.get_room_description())
