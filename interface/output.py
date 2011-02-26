#!/usr/bin/env python
from library.coord import *
from interface import console

screen = console.select()

def print_line (text, pos = POS_ORIGIN):
    """
    Prints a line of text beginning at the coordinate pos.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    """
    for ind, char in enumerate(text):
        screen.put(char, Coord(pos.x+ind, pos.y))

def print_text (text, pos = POS_ORIGIN, max_columns = 70):
    """
    Chops a text into several lines and prints it to the screen, beginning
    at coordinate pos. Chopping happens at position max_columns; no attempt
    is made to look for a better cutting position.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``max_columns``: After this column, the text is wrapped onto the next line. 
                      *Default 70*.
    """
    line = pos.y
    col  = 0
    for char in text:
        if (char == "\n" or col > max_columns):
            col   = 0
            line += 1
            if char == "\n":
               continue
        screen.put(char, Coord(col, pos.y + line))
        col += 1

def print_screen (text, pos = POS_ORIGIN, max_columns = 70):
    """
    Prints some text onto a cleared screen and waits for the player to press
    a key to leave the screen.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``max_columns``: After this column, the text is wrapped onto the next line. 
                      *Default 70*.
    """
    screen.clear(" ")
    print_text(text, pos)
    screen.get(block=True)
