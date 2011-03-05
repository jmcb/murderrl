#!/usr/bin/env python

from game import mainloop
from interface.menu import *
from interface import console

screen = console.select()

def main ():
    """
    Generate a manor and display all rooms in a scrollable menu.
    Choosing any of the rooms will display its description.
    """
    game  = mainloop.Game('H')
    rooms = game.base_manor.room_props

    m = ScrollMenu("Rooms")
    keyval = ord('a')
    for i in xrange(len(rooms)):
        key  = chr(keyval)
        e = Entry(key, rooms[i].name, rooms[i].describe)
        m.add_entry(e)

        if key == 'z':
            keyval = ord('A')
        else:
            keyval += 1

    screen.init()
    m.do_menu()
    screen.deinit()

if __name__ == "__main__":
    screen.wrapper(main)
