#!/usr/bin/env python

import unittest

from interface import screen, console
from library import coord

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

    def test_message_region (self):
        message_region = screen.MessageRegion(coord.Coord(0, 0), coord.Coord(20, 10), "messages", self.screen)
        self.screen.region(message_region)

        mr = self.screen.region_by_name("messages")

        for count in xrange(10):
            mr.append("This is a test")
        for count in xrange(5):
            mr.append("Why hello there")

        mr.blit()

        self.physical_screen.deinit()
        import pdb
        pdb.set_trace()

def main ():
    unittest.main()

if __name__=="__main__":
    main()
