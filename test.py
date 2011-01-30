#!/usr/bin/env python
import builder
import library.viewport, library.coord
import interface.console

a = builder.manor.build_U()
b = a.combine()
c = library.viewport.ViewPort(buffer=b)

screen = interface.console.select()

screen.init()
screen.put("test", library.coord.Coord(10, 10))
try:
    screen.get(block=True)
except:
    pass

screen.deinit()
