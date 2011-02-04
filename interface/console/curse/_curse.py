#!/usr/bin/env python
import library.coord as coord
import library.colour as colour
from library.colour import Colours
import curses

_STDSCREEN = None
_LASTCOLOUR = None

class CursesBaseColour (colour.BaseColour):
    def __init__ (self, colour):
        super(CursesBaseColour, self).__init__(colour._colour, colour._colour_id)

    def as_curses (self):
        c = self._colour

        if c == "black":
            return (curses.COLOR_BLACK, curses.A_NORMAL)
        elif c == "red":
            return (curses.COLOR_RED, curses.A_NORMAL)
        elif c == "green":
            return (curses.COLOR_GREEN, curses.A_NORMAL)
        elif c == "brown":
            return (curses.COLOR_YELLOW, curses.A_NORMAL)
        elif c == "blue":
            return (curses.COLOR_BLUE, curses.A_NORMAL)
        elif c == "magenta":
            return (curses.COLOR_MAGENTA, curses.A_NORMAL)
        elif c == "cyan":
            return (curses.COLOR_CYAN, curses.A_NORMAL)
        elif c == "lightgray":
            return (curses.COLOR_WHITE, curses.A_NORMAL)
        elif c == "darkgray":
            return (curses.COLOR_BLACK, curses.A_BOLD)
        elif c == "lightred":
            return (curses.COLOR_RED, curses.A_BOLD)
        elif c == "lightgreen":
            return (curses.COLOR_GREEN, curses.A_BOLD)
        elif c == "yellow":
            return (curses.COLOR_YELLOW, curses.A_BOLD)
        elif c == "lightblue":
            return (curses.COLOR_BLUE, curses.A_BOLD)
        elif c == "lightmagenta":
            return (curses.COLOR_MAGENTA, curses.A_BOLD)
        elif c == "lightcyan":
            return (curses.COLOR_CYAN, curses.A_BOLD)
        elif c == "white":
            return (curses.COLOR_WHITE, curses.A_BOLD)

class CursesColour (colour.Colour):
    def __init__ (self, colour):
        super(CursesColour, self).__init__(colour._foreground, colour._background, colour._style)

    def as_curses (self):
        fg, bold = CursesBaseColour(self._foreground).as_curses()
        bg = CursesBaseColour(self._background).as_curses()[0]

        return curses.color_pair(fg * 8 + bg) | bold

class InputError (Exception):
    pass

def _goto (c):
    _STDSCREEN.move(c.x, c.y)

def put (char, c, col=None):
    assert(len(char) == 1)

    global _LASTCOLOUR

    try:
        lcb = _LASTCOLOUR._background
    except:
        lcb = Colours.BLACK

    if col is not None:
        if isinstance(col, colour.BaseColour):
            col = colour.Colour(col, lcb)

        col = CursesColour(col)

        _LASTCOLOUR = col

        attr = col.as_curses()
    else:
        if _LASTCOLOUR is not None:
            attr = _LASTCOLOUR.as_curses()
        else:
            attr = 0

    curses.endwin()
    import pdb
    pdb.set_trace()

    _goto(c)

    _STDSCREEN.addch(ord(char), attr)

def get (err=False, block=False):
    if not block:
        _STDSCREEN.nodelay(1)

    ch = _STDSCREEN.getch()
    _STDSCREEN.nodelay(0)

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
    for a in xrange(8):
        for b in xrange(8):
            if a == 0 or b == 0:
                continue

            curses.init_pair(a * 8 + b, a, b)

    curses.init_pair(63, 0, 0);

def init ():
    global _STDSCREEN
    _STDSCREEN = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    _STDSCREEN.keypad(1)

def deinit ():
    curses.nocbreak()
    _STDSCREEN.keypad(0)
    curses.echo()
    curses.endwin()

def size ():
    pass
