#!/usr/bin/env python
import library.coord as coord

def put (char, c, colour=None):
    pass

def get (err=False):
    pass

def clear (char=None, colour=None):
    termsize = size()

    for x in xrange(termsize.width):
        for y in xrange(termsize.height):
            put (char, coord.Coord(x, y), colour)

def init ():
    pass

def deinit ():
    pass
