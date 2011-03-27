#!/usr/bin/env python
from library.coord import *
from interface import console
from library.colour import Colours

screen = console.select()

def print_line (text, pos = POS_ORIGIN, colour = Colours.LIGHTGRAY):
    """
    Prints a line of text beginning at the coordinate pos.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``col``: The output colour. *Default lightgray*.
    """
    for ind, char in enumerate(text):
        screen.put(char, Coord(pos.x+ind, pos.y), colour)

def print_text (text, pos = POS_ORIGIN, max_columns = 70, colour = Colours.LIGHTGRAY):
    """
    Chops a text into several lines and prints it to the screen, beginning
    at coordinate pos. Chopping happens at position max_columns; no attempt
    is made to look for a better cutting position.

    :``text``: The text to be printed. *Required*.
    :``pos``: The starting coord (of type ``Coord``) for printing. *Default (0,0)*.
    :``max_columns``: After this column, the text is wrapped onto the next line. 
                      *Default 70*.
    """
    col     = 0
    lastcol = 0
    for char in text:
        if char == "\n":
            print_line(text[:col], pos, colour)
            print_text(text[col+1:], Coord(pos.x, pos.y+1), max_columns, colour)
            return

        if char == " ":
            last_col = col

        if col > max_columns:
            print_line(text[:last_col], pos, colour)
            print_text(text[last_col+1:], Coord(pos.x, pos.y+1), max_columns, colour)
            return

        col += 1

    print_line(text, pos, colour)

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
