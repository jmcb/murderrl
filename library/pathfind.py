#!/usr/bin/env python

from library import feature, coord

INFINITY = 10000
class Grid (object):
    def __init__ (self, size, value = None):
        self.grid = []
        self._width  = size.x
        self._height = size.y
        for row in xrange(size.x):
            row = []
            for column in xrange(size.y):
                row.append(value)
            self.grid.append(row)

    def size (self):
        return coord.Coord(self._width, self._height)

    def __getvalue__ (self, pos):
        # assert isinstance(pos, coord.Coord)
        assert (pos.y < self._height)
        assert (pos.x < self._width)
        return self.grid[pos.y][pos.x]

    def __setvalue__ (self, pos, value):
        # assert isinstance(pos, coord.Coord)
        assert (pos.y < self._height)
        assert (pos.x < self._width)
        self.grid[pos.y][pos.x] = value

class DistanceGrid (Grid):
    def __init__ (self, size, value = INFINITY):
        Grid.__init__(self, size, value)

class PrevGrid (Grid):
    pass

class Pathfind (object):
    def __init__ (self, grid, start, target):
        self.fgrid     = grid
        # Yes, they are swapped. Makes for easier backtracking.
        self.start     = target
        self.target    = start
        self.dgrid     = DistanceGrid(self.fgrid.size(), INFINITY)
        self.pgrid     = PrevGrid(self.fgrid.size())

    def path_exists (self):
        if self.start == self.target:
            return True

        return self.pathfind() != None

    def get_path (self):
        if self.start == self.target:
            return [self.start]

        if self.pathfind() == None:
            return None
        path = self.backtrack(self.target)
        return path

    def backtrack (self, begin):
        path = []
        next = begin
        while next != None:
            path.append(next)
            next = self.pgrid.__getvalue__(next)
        return path

    def add_neighbours (self, curr):
        for pos in coord.AdjacencyIterator(curr):
            if not self.fgrid.__getitem__(pos).traversable():
                continue
            new_dist = self.dgrid.__getvalue__(curr) + 1
            if pos in self.nlist:
                if self.dgrid.__getvalue__(pos) > new_dist:
                    # print "Old distance(%s): %s, old prev: (%s)" % (pos, self.dgrid.__getvalue__(pos), self.pgrid.__getvalue__(pos))
                    self.dgrid.__setvalue__(pos, new_dist)
                    self.pgrid.__setvalue__(pos, curr)
                    # print "Change distance(%s) to %s, prev to (%s)" % (pos, new_dist, curr)
            elif self.dgrid.__getvalue__(pos) == INFINITY:
                # print "Set distance(%s) to %s, prev to (%s)" % (pos, new_dist, curr)
                self.dgrid.__setvalue__(pos, new_dist)
                self.pgrid.__setvalue__(pos, curr)
                self.nlist.append(pos)
            if pos == self.target:
                return True
        return False

    def pathfind (self):
        self.nlist = [self.start]
        self.dgrid.__setvalue__(self.start, 0)

        while len(self.nlist) > 0:
            curr = self.nlist[0]
            self.nlist.remove(curr)
            if self.add_neighbours(curr):
                return curr
            self.nlist.sort(cmp=lambda a, b: cmp(self.dgrid.__getvalue__(a), self.dgrid.__getvalue__(b)))
        return None
