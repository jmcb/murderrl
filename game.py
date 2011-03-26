#!/usr/bin/env python
"""
Play the actual game. Let the sleuthing begin!
"""

import interface.console
from game import mainloop

screen = interface.console.select()

def main ():
    screen.init()
    game = mainloop.Game()
    game.do_loop()
    screen.deinit()

if __name__ == "__main__":
    screen.wrapper(main)
