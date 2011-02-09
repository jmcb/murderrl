#!/usr/bin/env python

import database.database as db
from suspects.person import *
from interface.menu import *

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

    print rooms
    return rooms

def main (num = 10):
    """
    Generate a list of suspects and display them in a menu.
    Choosing any of the suspects will display further information about them.

    :``num``: The number of suspects to be generated. *Default 10*.
    """
    rooms = get_rooms(num)
    sl    = SuspectList(num, rooms)

    m = Menu("Suspects")
    e = Entry('x', "Victim: " + str(sl.get_victim()), sl.describe_suspect, sl.victim, 'v')
    m.add_entry(e)
    total_suspects = xrange(len(sl.suspects))
    count = 0
    for i in total_suspects:
        if not sl.is_victim(i):
            p = sl.get_suspect(i)
            e = Entry(chr(ord('a') + count), p, sl.describe_suspect, i)
            count += 1
            m.add_entry(e)
    m.do_menu()

def alpha_main (num = 10):
    """
    Generate a list of suspects and display them in a menu.
    Choosing any of the suspects will display further information about them.

    :``num``: The number of suspects to be generated. *Default 10*.
    """
    rooms = get_rooms(num)
    sl    = SuspectList(num, rooms)

    m = Menu("Suspects")
    e = Entry('x', "Victim: " + str(sl.get_victim()),
              sl.describe_suspect, sl.victim, sl.get_victim().first[0].lower())
    m.add_entry(e)

    # Construct a list of (index, first name) tuples.
    name_list = []
    for i in xrange(sl.no_of_suspects()):
        name_list.append((i, sl.get_suspect(i).first))

    # Sort the list by name.
    name_list.sort(key=lambda person: person[1])

    total_suspects = xrange(len(sl.suspects))
    for i in xrange(sl.no_of_suspects()):
        idx = name_list[i][0]
        if not sl.is_victim(idx):
            p = sl.get_suspect(idx)
            e = Entry(p.first[0].lower(), p, sl.describe_suspect, idx)
            m.add_entry(e)
    m.do_menu()

if __name__ == "__main__":
    """
    Generate a list of suspects and display them in a menu.
    Choosing any of the suspects will display further information about them.

    :``num``: The number of suspects to be generated. *Default 10*.
    """
    import sys

    # As each letter can only be used once, there's a fixed cap
    # at 26 suspects, but seeing how some letters are really rare
    # (or have no names assigned) we should not try for more than
    # around 20.
    max_suspects = 10
    if len(sys.argv) > 1:
        try:
            max_suspects = min(int(sys.argv[1]), 20)
        except ValueError:
            sys.stderr.write("Warning: Expected integer argument, using default value %d\n" % max_suspects)
            pass

    alpha_main(max_suspects)
