#!/usr/bin/env python


import random
from library import shape, coord
import database.database as db

ROOM_WIDTH  = 12
ROOM_HEIGHT = 7

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
        self.name = name
        Room.__init__(self, width, height, start)

    def __repr__ (self):
        if self.name:
            return self.name
        return "buggy crawl space"

    def mark_as_corridor (self, is_corridor = True):
        self.is_corridor = is_corridor

    def is_corridor (self):
        if self.is_corridor:
            return self.is_corridor
        return False

    def fill_from_database (self):
        """
        Pull a random room name from the database.
        """
        dbr      = db.get_database("rooms")
        new_room = dbr.random_pop()
        if (new_room):
            self.name = new_room.name
            if new_room.section == "utility":
                self.utility = True
