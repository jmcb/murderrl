#!/usr/bin/env python

import unittest

from interface import screen, console, regions
from library import coord, shape

class RegionTest (unittest.TestCase):
    """
    This test ensures that all of the region set-up and code works as expected
    and results in the correct information and text being drawn to the correct
    area of the screen.
    """

    def setUp (self):
        self.physical_screen = console.select()

        self.physical_screen.init()
        self.screen = screen.Screen(self.physical_screen.size(), self.physical_screen)

    def tearDown (self):
        self.physical_screen.deinit()
        pass

    def test_message_region (self):
        message_region = regions.MessageRegion(coord.Coord(0, 0), coord.Coord(5, 5), "messages", self.screen)
        self.screen.region(message_region)

        mr = self.screen.region_by_name("messages")

        mr.append("This is a test of wrapping.")

        result = shape.Shape(["is a ", "test ", "of wr", "appin", "g.   "])
        self.assertEqual(mr.as_shape()._canvas, result._canvas)

        mr.blit()
        self.screen.blit()

        self.physical_screen.get(block=True)

def main ():
    unittest.main()

if __name__=="__main__":
    main()
