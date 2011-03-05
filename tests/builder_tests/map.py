#!/usr/bin/env python
"""
Outputs a map of the furnished manor, annotated with room numbers and names.
"""

from builder import manor
from library import coord
from library.feature import *
from interface.features import *
from suspects import person

def build_manor (type):
    m = manor.builder_by_type(type)

    # Add doors and windows, etc.
    m.add_features()

    # Add bed rooms for a number of suspects.
    sl = person.SuspectList(10)
    list = sl.get_id_name_tuples()
    m.init_room_names(list)

    return m

def draw_number (canvas, pos, number):
    single = number % 10
    digit  = number/10
    if digit != 0:
        canvas.__setitem__(pos, str(digit))
    canvas.__setitem__(coord.Coord(pos.x+1,pos.y), str(single))

def add_symbol (canvas, pos, char):
    canvas.__setitem__(coord.Coord(pos.x+2,pos.y), char)

def main (type):
    m = build_manor(type)

    canvas = m.combine()

    # Draw features on canvas.
    for pos in coord.RectangleIterator(canvas.size()):
        feat = m.get_feature(pos)
        if feat != NOTHING and feat != WALL and feat != FLOOR:
            canvas.__setitem__(pos, feat.glyph())

    for r in m.rooms:
        room   = m.get_room(r)
        centre = coord.Coord(room.pos().x + room.size().x/2 - 1, room.pos().y + room.size().y/2)
        draw_number(canvas, centre, r)
        if r == m.entrance_hall:
            add_symbol(canvas, centre, "E")
        else:
            rp = m.room_props[r]
            if rp.section == "utility":
                add_symbol(canvas, centre, "U")
            elif rp.name.endswith("bedroom"):
                add_symbol(canvas, centre, "B")

    print canvas

    print "\n"
    for r in xrange(len(m.room_props)):
        name = m.room_props[r].name
        r_str = " "
        if r < 10:
            r_str += str(r)
        else:
            r_str = str(r)
        print "%s. %s" % (r_str, name)
    print "\nE = entrance hall, B = bedroom, U = utility section"

if __name__ == "__main__":

    import sys
    type = ""
    if len(sys.argv) > 1:
        type = sys.argv[1].upper()

    main(type)
