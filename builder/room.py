#!/usr/bin/env python

import random
from library import shape, coord
import database.database as db
from interface.output import *

ROOM_WIDTH  = 12
ROOM_HEIGHT = 7

def join_strings (list):
    if len(list) == 0:
        return ""

    if len(list) == 1:
        return list[0]

    result = list[0]
    last   = list[-1]
    for i in xrange(1,len(list)-1):
        result += ", %s" % list[i]
    result += ", and %s" % last

    return result

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

class RoomProps (Room):
    def __init__ (self, name=None, start=None, width=ROOM_WIDTH, height=ROOM_HEIGHT):
        Room.__init__(self, width, height, start)
        self.init_db_props(name, "corridor")

        # Initialise a few variables for later.
        self.adj_rooms = []
        self.adj_room_names = []

    def init_db_props(self, name, section=None):
        self.name    = name
        self.section = section

    def __str__ (self):
        if self.name:
            return self.name
        return "buggy crawl space"

    def mark_as_corridor (self, is_corridor = True):
        self.is_corridor = is_corridor

    def is_corridor (self):
        if self.is_corridor:
            return self.is_corridor
        return False

    def add_adjoining_room (self, ridx):
        if not ridx in self.adj_rooms:
            self.adj_rooms.append(ridx)

    def add_adjoining_room_name (self, name):
        self.adj_room_names.append(name)
        assert(len(self.adj_rooms) >= len(self.adj_room_names))

    def fill_from_database (self):
        """
        Pull a random room name from the database.
        """
        dbr      = db.get_database("rooms")
        new_room = dbr.random_pop()
        if new_room:
            print new_room.name
            self.init_db_props(new_room.name, new_room.section)

    def get_room_description (self):
        """
        Returns a room's description.
        """
        # Very basic right now, but will eventually include adjoining rooms
        # and furniture.
        desc = "You are standing in the %s.\n\n" % self.name
        desc += "It is part of the manor's %s area.\n\n" % self.section

        if len(self.adj_rooms) > 0:
            desc += "There "
            if len(self.adj_rooms) == 1:
                desc += "is a door"
            else:
                desc += "are doors"
            assert(len(self.adj_room_names) > 0)
            desc += " leading to the %s." % join_strings(self.adj_room_names)

        return desc

    def describe (self):
        """
        Print a room description.
        """
        print_screen(self.get_room_description())
