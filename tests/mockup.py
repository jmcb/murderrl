#!/usr/bin/env python
"""
A demo of our @ detective walking through an otherwise empty manor. :P
Toggle canvas vs. feature view with 't'. (Should be identical.)
"""

import interface.console
from game import mainloop

screen = interface.console.select()

def main ():
    screen.init()
    game = mainloop.Game()
    game.do_loop()
    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
