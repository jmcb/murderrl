#!/usr/bin/env python
import library.coord as coord
import curses

STDSCREEN = None
COLOURS = {}

class InputError (Exception):
    pass

def _goto (c):
    STDSCREEN.move(c.x, c.y)

def put (char, c, colour=None):
    STDSCREEN.addstr(c.x, c.y, char)

def get (err=False, block=False):
    if not block:
        STDSCREEN.nodelay(1)

    ch = STDSCREEN.getch()
    STDSCREEN.nodelay(0)

    if ch == curses.ERR:
        if err:
            raise InputError
        else:
            return None
    else:
        return ch

def clear (char=None, colour=None):
    termsize = size()

    for x in xrange(termsize.width):
        for y in xrange(termsize.height):
            put (char, coord.Coord(x, y), colour)

def _init_colours ():
    

def init ():
    global STDSCREEN
    STDSCREEN = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    STDSCREEN.keypad(1)

def deinit ():
    curses.nocbreak()
    STDSCREEN.keypad(0)
    curses.echo()
    curses.endwin()

def size ():
    pass
