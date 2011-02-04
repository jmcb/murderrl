#!/usr/bin/env python
import builder
import library.viewport, library.coord, library.colour
from library.colour import Colours
import interface.console

a = builder.manor.build_U()
b = a.combine()
c = library.viewport.ViewPort(buffer=b)

screen = interface.console.select()

c = library.colour.Colour(Colours.GREEN, Colours.BLUE)

screen.init()
screen.put("t", library.coord.Coord(10, 10), c)
screen.put("e", library.coord.Coord(10, 11), c)

try:
    screen.get(block=True)
except:
    pass

screen.deinit()
