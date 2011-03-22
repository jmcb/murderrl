#!/usr/bin/env python

from library import coord, feature, pathfind
from interface.features import *

class PathfindTest (object):
    def __init__ (self):
        self.init_fgrid()
        self.fgrid.draw()
        self.counter_wrong = 0
        self.counter_right = 0

        A = coord.Coord(1,8)
        B = coord.Coord(1,1)
        C = coord.Coord(2,4)
        D = coord.Coord(6,1)
        E = coord.Coord(8,1)
        self.pathfind_test(A, A, True)
        self.pathfind_test(A, B, False)
        self.pathfind_test(B, A, False)
        self.pathfind_test(B, D, True)
        self.pathfind_test(D, B, True)
        self.pathfind_test(B, C, False)
        self.pathfind_test(C, B, False)
        self.pathfind_test(D, E, True)
        self.pathfind_test(E, D, True)

    def evaluate (self):
        print "counter right: %s" % self.counter_right
        print "counter wrong: %s" % self.counter_wrong
        return self.counter_wrong == 0

    def init_fgrid (self):
        ##########
        #B...#D#E#
        #..#...#.#
        ###....#.#
        ##C#...#.#
        #.####.#.#
        #......#.#
        ###.####.#
        #A#......#
        ##########
        self.fgrid = feature.FeatureGrid(10, 10, WALL)
        for pos in coord.RectangleIterator(coord.Coord(1,1), coord.Coord(9,9)):
            self.fgrid.__setitem__(pos, FLOOR)
        self.fgrid.__setitem__(coord.Coord(5,1), WALL)
        self.fgrid.__setitem__(coord.Coord(3,2), WALL)
        self.fgrid.__setitem__(coord.Coord(1,3), WALL)
        self.fgrid.__setitem__(coord.Coord(2,3), WALL)
        self.fgrid.__setitem__(coord.Coord(1,4), WALL)
        self.fgrid.__setitem__(coord.Coord(3,4), WALL)
        for pos in coord.RectangleIterator(coord.Coord(7,1), coord.Coord(8,8)):
            self.fgrid.__setitem__(pos, WALL)
        for pos in coord.RectangleIterator(coord.Coord(2,5), coord.Coord(6,6)):
            self.fgrid.__setitem__(pos, WALL)
        for pos in coord.RectangleIterator(coord.Coord(1,7), coord.Coord(3,9)):
            self.fgrid.__setitem__(pos, WALL)
        for pos in coord.RectangleIterator(coord.Coord(4,7), coord.Coord(8,8)):
            self.fgrid.__setitem__(pos, WALL)
        self.fgrid.__setitem__(coord.Coord(1,8), FLOOR)

    def pathfind_test (self, start, stop, expected):
        result = pathfind.Pathfind(self.fgrid, start, stop).path_exists()
        if result:
            print "A path between %s and %s exists." % (start, stop)
            print pathfind.Pathfind(self.fgrid, start, stop).get_path()
        else:
            print "A path between %s and %s could not be found." % (start, stop)

        if result == expected:
            self.counter_right += 1
        else:
            self.counter_wrong += 1

if __name__ == "__main__":
    if PathfindTest().evaluate():
        print "The pathfinding test was successful."
    else:
        print "There were errors in the pathfinding test."
