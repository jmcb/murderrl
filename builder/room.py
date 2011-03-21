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

    return "%s and %s" % (', '.join(list[:-1]), list[-1])

def pluralise (word):
    if word[-1] == 'f':
        return "%sves" % word[:-1]
    return "%ss" % word

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

class DB_Room (object):
    """
    A database representation of a room, used to compare actual room layout
    with room type properties returned by the database.
    """
    def __init__ (self, want_utility=None, is_passage=False, size=None, has_windows=None, debug=False):
        """
        Initialise the room type requirements.

        :``size``: The room size, compared against minimum and maximum room size. *Default None*.
        :``is_passage``: If true, try to pick passage rooms. *Default False*.
        :``has_windows``: If true, try to pick a room type with windows. If None, we don't care whether it has windows or not. *Default None*.
        :``want_utility``: If true, prefer utility room types. If false, prefer domestic room types. Otherwise, we don't care. *Default None*.
        :``debug``: If true, print debugging statements. *Default False*.
        """
        self.size    = size
        self.passage = is_passage
        self.windows = has_windows
        self.utility = want_utility
        self.debug   = debug
        if self.debug:
            print "initialise db_room with size: %s, passage: %s, windows: %s, utility: %s" % (size, is_passage, has_windows, want_utility)

    def check_room (self, db_room):
        """
        Compares a set of room properties returned by the database against the
        defined requirements.

        :``db_room``: The room type picked from the database. *Required*.
        """
        if self.utility != None and self.utility != (db_room.section == "utility"):
            return False

        if self.size != None and (self.size < db_room.min_size or self.size > db_room.max_size):
            return False

        if self.passage and not db_room.is_passage:
            return False

        if self.windows != None and self.windows != db_room.has_windows:
            return False

        return True

    def pick_room (self):
        """
        Pick a room type from the database that matches the requirements.
        If no applicable room can be found, loosen the requirements one after another.
        """
        dbr = db.get_database("rooms")

        new_room = dbr.random_pop(self.check_room)
        if new_room == None:
            # Loosen restrictions in order of importance.
            if self.windows != None:
                if self.debug:
                    print "loosen windows restriction"
                self.windows = None
            elif self.size != None:
                if self.debug:
                    print "loosen size restriction"
                self.size = None
            elif self.passage:
                if self.debug:
                    print "loosen passage restriction"
                self.passage = False
            # Section checks override all other checks.
            elif self.utility != None:
                if self.debug:
                    print "loosen utility restriction"
                self.utility = None
            else:
                if self.debug:
                    print "get random room"
                return dbr.random_pop()

            return self.pick_room()

        if self.debug:
            print "found room: %s" % new_room
        return new_room

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
        self.furniture      = []

    def init_db_props(self, name, section=None, prep="in", complete=False):
        self.name       = name
        self.section    = section
        self.prep       = prep # preposition
        self.has_data   = complete

    def __str__ (self):
        return self.name

    def room_name (self, article=False):
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

    def add_furniture_name (self, name):
        for f in xrange(len(self.furniture)):
            if name in self.furniture[f]:
                plural = pluralise(name)
                # A bit of a hack!
                if "two" in self.furniture[f]:
                    self.furniture[f] = "some " % plural
                else:
                    self.furniture[f] = "two %s" % plural
                return

        self.furniture.append("a %s" % name)

    def is_good_bedroom (self, check_windows=True, max_size=None):
        # May not be a passage room, doesn't need to be large, needs windows.
        if len(self.adj_rooms) > 1:
            return False

        if check_windows and len(self.windows) == 0:
            return False

        if max_size and self.width * self.height > max_size:
            return False

        return True

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

        db_room = DB_Room(want_utility = utility, is_passage=len(self.adj_rooms) > 1,
        size=self.width * self.height, has_windows = len(self.windows) > 0, debug=True)

        new_room = db_room.pick_room()
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
        desc += "It is part of the manor's %s area.\n\n" % self.section

        if len(self.furniture) == 0:
            desc += "It is completely unfurnished.\n"
        else:
            desc += "You see here %s.\n" % join_strings(self.furniture)
        desc += "%s\n\n" % self.describe_windows()

        desc += self.describe_exits()

        return desc

    def describe (self):
        """
        Print a room description.
        """
        print_screen(self.get_room_description())
