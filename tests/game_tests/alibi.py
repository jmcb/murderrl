#!/usr/bin/env python
"""
Outputs a map of the furnished manor, annotated with room numbers and names.
"""

import random
from builder import manor
from game import mainloop
from library import coord
from library.feature import *
from library.random_util import *
from interface.features import *
from suspects import person

def build_manor (type):
    m = manor.builder_by_type(type)

    # Add doors and windows, etc.
    m.add_features()

    return m

def draw_number (canvas, pos, number):
    """
    Draw a number with up to two digits in a given position.
    """
    single = number % 10
    digit  = number/10
    if digit != 0:
        canvas.__setitem__(pos, str(digit))
    canvas.__setitem__(coord.Coord(pos.x+1,pos.y), str(single))

def add_symbol (canvas, pos, char):
    """
    Draw a symbol slightly off-centre of a room.
    """
    canvas.__setitem__(coord.Coord(pos.x+2,pos.y), char)

def draw_alibi_rooms(canvas, sl, m):
    """
    Draws a map of the manor, while adding symbols for alibis and room types.
    """
    murder_room = sl.get_victim().alibi.rid
    # Get a list of alibi rooms matching each suspect id.
    alibis = []
    for s in sl.suspects:
        a = s.alibi
        if a == None:
            print "No alibi for suspect %s" % s.get_name()
            alibis.append(-1)
        else:
            alibis.append(a.rid)

    # Add letters depicting murder room, alibis, and other stuff.
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

        if r == murder_room:
            canvas.__setitem__(coord.Coord(centre.x+1,centre.y+1), "X")
        else:
            count = 1
            # Alibi room for which suspects?
            for i in range(0, len(alibis)):
                if r == alibis[i]:
                    char = sl.get_suspect(i).first[0]
                    canvas.__setitem__(coord.Coord(centre.x+count,centre.y+1), char)
                    count += 1

    print canvas, "\n"

    # List the rooms and the suspects referring to them in their alibi.
    for r in xrange(len(m.room_props)):
        name = m.room_props[r].name
        r_str = " "
        if r < 10:
            r_str += str(r)
        else:
            r_str = str(r)
        desc = "%s. %s" % (r_str, name)
        if r in m.rooms:
            if r == murder_room:
                desc += " (murder room)"
            else:
                who = []
                for i in xrange(len(alibis)):
                    if alibis[i] == r:
                        who.append(sl.get_suspect(i).get_name())
                if len(who) > 0:
                    desc += " (Alibi for: %s)" % ', '.join(who)
            print desc

    # A legend for the various symbols.
    print "\nE = entrance hall, B = bedroom, U = utility section"
    print "X = site of crime, other letters: suspects' alibi rooms"

def main (type):
    game = mainloop.Game(type)
    draw_alibi_rooms(game.canvas, game.suspect_list, game.base_manor)

if __name__ == "__main__":

    import sys
    type = ""
    if len(sys.argv) > 1:
        type = sys.argv[1].upper()

    main(type)
