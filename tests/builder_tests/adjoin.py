#!/usr/bin/env python
"""
unit test for manor building.
"""

from builder import room, builder
from library import shape

if __name__=="__main__":

    width1 = 8
    width2 = 10
    print "width1: %s, width2: %s" % (width1, width2)
    overlaps = [-1, 0, 1]
    for o in overlaps:
        print "\noverlap = %s:" % o
        room1 = room.Room(width=width1).as_shape()
        room2 = room.Room(width=width2).as_shape()
        combined = shape.adjoin(room1, room2, overlap=o, collect=True)
        m = builder.BuilderCollection(combined)
        print m.combine()
        for r in m.rooms:
            rm = m.get_room(r)
            print "Room %s: width=%s, start=(%s), end=(%s)" % (r, rm.width(), rm.pos(), rm.pos() + rm.size() - 1)
