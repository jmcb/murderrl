#!/usr/bin/env python
from library.coord import *
from interface import console
from library.colour import Colours

screen = console.select()

def print_line (text, pos = POS_ORIGIN, col = Colours.LIGHTGRAY):
    """
    Prints a line of text beginning at the coordinate pos.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``col``: The output colour. *Default lightgray*.
    """
    for ind, char in enumerate(text):
        screen.put(char, Coord(pos.x+ind, pos.y), col)

def print_text (text, pos = POS_ORIGIN, max_columns = 70, col = Colours.LIGHTGRAY):
    """
    Chops a text into several lines and prints it to the screen, beginning
    at coordinate pos. Chopping happens at position max_columns; no attempt
    is made to look for a better cutting position.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``max_columns``: After this column, the text is wrapped onto the next line. 
                      *Default 70*.
    """
    line   = pos.y
    column = pos.x
    for char in text:
        if (char == "\n" or column > max_columns):
            column = pos.x
            line  += 1
            if char == "\n":
               continue
        screen.put(char, Coord(column, line), col)
        column += 1

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

def highlight_colour (highlight):
    if highlight == True:
        return Colours.WHITE
    elif highlight == False:
        return Colours.DARKGRAY
    else:
        return Colours.LIGHTGRAY
