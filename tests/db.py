#!/usr/bin/env python

import sys
import random
import database.database as db

def check_for_utility (db_room):
    return db_room.section == "utility"

def alphabetic_check (db_room):
    return db_room.name[0] <= "c"

def check_is_passage (db_room):
    return db_room.is_passage

def check_no_windows (db_room):
    return not db_room.has_windows

def get_room_from_database (try_strict, type = "utility"):
    """
    Pulls a random room matching some kind of criterion from the database.
    If none can be found, try again without the additional requirements.
    
    :``try_strict``: If true, apply a function to check for some requirement.
                     If the results is None, print a message and return
                     False. If false, just get a random room. *Required*.
    """
    dbr = db.get_database("rooms")
    if try_strict:
        if type == "utility":
            new_room = dbr.random_pop(check_for_utility)
        elif type == "passage":
            new_room = dbr.random_pop(check_is_passage)
        elif type == "no_windows":
            new_room = dbr.random_pop(check_no_windows)
        else:
            new_room = dbr.random_pop(alphabetic_check)

        if new_room == None:
            print "None found -> relax the requirements:",
            get_room_from_database(False)
            return False
    else:
        new_room = dbr.random_pop()

    print new_room.name
    return try_strict
        
def main (type):
    print "Rooms matching the '%s' criterion:" % type
    try_strict = True
    for i in xrange(10):
        try_strict = get_room_from_database(try_strict, type)

if __name__ == "__main__":

    types = ["utility", "no_windows", "passage", "alphabetic"]
    type  = types[0]

    if len(sys.argv) > 1:
        val = sys.argv[1]
        if val not in types:
            sys.stderr.write("Error: No type '%s' in %s. Using '%s' instead.\n\n" % (val, types, type))
        else:
            type = val

    main(type)
        