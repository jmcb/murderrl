#!/usr/bin/env python
import builder
import library.viewport, library.coord, library.colour
from library.colour import Colours
import interface.console

a = builder.manor.build_U()
b = a.combine()
c = library.viewport.ViewPort(buffer=b)

screen = interface.console.select()

def main ():
    screen.init()

    screen.clear("X", library.colour.Colour(Colours.LIGHTGRAY, Colours.LIGHTGRAY))

    try:
        screen.get(block=True)
    except:
        pass

    screen.deinit()

screen.wrapper(main)
