#!/usr/bin/env python
"""
A mockup of the complete mystery, alibis, murderer, and all.
"""

import database.database as db
from suspects.person import *

def get_rooms (num = 10):
    """
    Pull a random list of room names from the database.

    :``num``: The number of suspects. *Default 10*.
    """
    # Note: Instead of pulling up random room names from the database,
    #       this should eventually draw on the manor's room list.
    rooms = []
    dbr   = db.get_database("rooms")
    for i in xrange(num):
        new_room = dbr.random_pop()
        if (new_room):
            new_room = new_room.name
        else:
            new_room = "nowhere"
        rooms.append(new_room)

    return rooms

def print_mystery(self, num = 10):
    """
    Generates a set of suspects, their alibis and hair colours, and
    outputs the result.

    :``num``: The number of suspects. *Default 10*.
    """
    rooms = get_rooms(num)
    sl    = SuspectList(num, rooms)

    print "The victim: %s, %s" % (sl.get_victim().get_name(),
                                  sl.get_victim().describe_hair())

    total_suspects = xrange(len(sl.suspects))
    print_header("All suspects");
    for i in total_suspects:
        if not sl.is_victim(i):
            p = sl.get_suspect(i)
            print "%s, %s" % (p.get_name(), p.describe_hair())

    print "\nThe clue: a %s hair!" % sl.get_murderer().hair

    confirmed   = sl.get_cleared_suspects()
    print_header("Confirmed alibis");
    sl.print_alibis(confirmed)

    unconfirmed = list(set(total_suspects) - set(confirmed))
    print_header("Unconfirmed alibis");
    sl.print_alibis(unconfirmed)

    print "\nThe murderer:", sl.get_murderer().get_name()

if __name__ == "__main__":
    import sys

    max_suspects = 10
    if len(sys.argv) > 1:
        try:
            max_suspects = min(int(sys.argv[1]), 20)
        except ValueError:
            sys.stderr.write("Warning: Expected integer argument, using default value %d\n" % max_suspects)
            pass

    print_mystery(max_suspects)
