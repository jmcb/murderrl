#!/usr/bin/env python
import curses

import builder.manor
import library.viewport, library.coord
import interface.console

screen = interface.console.select()

def put_text (text, spot):
    for ind, char in enumerate(text):
        screen.put(char, library.coord.Coord(spot.x+ind, spot.y))

def main ():
    screen.init()

    manor = builder.manor.build_U().combine()

    vp = library.viewport.ViewPort(buffer=manor, width=60, height=15)

    while True:
        screen.clear("-")

        sect = vp.sect()

        for coord, char in sect:
            if char == None:
                char = " "
            screen.put(char, coord+1)

        put_text("Sect size: %s, Start coord: %s, Stop coord: %s" % (sect.size(), library.coord.Coord(vp._left, vp._top), library.coord.Coord(vp._left + vp._width, vp._top + vp._height)), library.coord.Coord(0, 23))

        ch = screen.get(block=True)

        if ch == curses.KEY_UP:
            vp.up(1)
        elif ch == curses.KEY_DOWN:
            vp.down(1)
        elif ch == curses.KEY_LEFT:
            vp.left(1)
        elif ch == curses.KEY_RIGHT:
            vp.right(1)
        else:
            break

    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
