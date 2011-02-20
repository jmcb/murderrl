#!/usr/bin/env python
"""
A demo of our @ detective walking through an otherwise empty manor. :P
Toggle canvas vs. feature view with 't'. (Should be identical.)
"""

import curses

import builder.manor
import library.viewport, library.coord
import interface.console
from interface.features import *

screen = interface.console.select()

def put_text (text, spot):
    for ind, char in enumerate(text):
        screen.put(char, library.coord.Coord(spot.x+ind, spot.y))

def is_traversable (feature_grid, pos):
    return feature_grid.__getitem__(pos).traversable()

def main ():
    screen.init()

    # First, build the manor.
    # base_manor = builder.manor.base_builder()
    base_manor = builder.manor.build_random()

    # Translate rooms and corridors into wall and floor features.
    base_manor.init_features()
    # Add doors along corridors.
    base_manor.add_doors()
    # Combine the room shapes into a canvas.
    manor = base_manor.combine()

    # Draw doors onto the canvas.
    for c in base_manor.doors:
        if c.x < 1 or c.x >= manor.size().x or c.y < 1 or c.y >= manor.size().y:
            print "Coord %s out of bounds %s" % (c, manor.size())
            continue
        manor.__setitem__(c, '+')

    # Initialise the view port.
    vp = library.viewport.ViewPort(buffer=manor,
                                   width =min(manor.size().width, 70),
                                   height=min(manor.size().height, 20))

    # Place the player on the first door we see.
    size = vp.sect().size()
    for coord in library.coord.RectangleIterator(size - 1):
        if base_manor.features.__getitem__(coord) == CLOSED_DOOR:
            ppos = coord # player (@) position in the viewport
            break

    # Initialise a couple of other variables.
    last_move = library.coord.Coord(0, 0) # the last step taken by the player
    move_was_blocked = False # tried to leave the manor boundaries
    did_move         = True  # actually took a step
    print_features   = False # draw manor via the feature grid
    while True:
        screen.clear(" ")

        # The currently visible section of the viewport.
        sect = vp.sect()

        # The real player position in the manor.
        real_pos = library.coord.Coord(vp._left + ppos.x + 1, vp._top + ppos.y + 1)

        # Depending on the current toggle state (toggle key 't'), either draw
        # the manor via the feature grid, or via the shape canvas.
        if print_features:
            for coord in library.coord.RectangleIterator(sect.size()):
                if coord >= base_manor.features.size():
                    continue
                real_coord = coord + library.coord.Coord(vp._left, vp._top)
                char = base_manor.features.__getitem__(real_coord).glyph()
                if coord == ppos:
                    if (move_was_blocked
                    or not is_traversable(base_manor.features, real_coord)):
                        ppos = ppos - last_move
                        char = "X"
                screen.put(char, coord+1)
        else:
            for coord, char in sect:
                if char == None:
                    char = " "
                if coord == ppos:
                    real_coord = coord + library.coord.Coord(vp._left, vp._top)
                    if (move_was_blocked
                    or not is_traversable(base_manor.features, real_coord)):
                        ppos = ppos - last_move
                        char = "X"
                screen.put(char, coord+1)

        # Draw the player.
        screen.put("@", ppos + 1)

        # Debugging information.
        put_text("Sect size : %s, Start coord: %s, Stop coord: %s" % (sect.size(), library.coord.Coord(vp._left, vp._top), library.coord.Coord(vp._left + vp._width, vp._top + vp._height)), library.coord.Coord(0, 23))

        # Get the current room/corridor id.
        id = base_manor.get_corridor_index(real_pos)
        type = "corridor"
        if id == None:
            id   = base_manor.get_room_index(real_pos)
            type = "room"
        put_text("Manor size: %s, Player coord: %s, last_move: %s, %s id: %s" % (manor.size(), real_pos, last_move, type, id), library.coord.Coord(0, 24))

        # Get a key.
        ch = screen.get(block=True)

        # Move the player (@) via the arrow keys.
        # If we haven't reached the manor boundaries yet, scroll in that direction.
        # Otherwise, take a step unless it would make us leave the manor.

        # Reinitialise the relevant variables.
        last_move        = library.coord.Coord(0, 0)
        move_was_blocked = False
        did_move         = True
        if ch == curses.KEY_UP:
            last_move.y = -1
            if vp._top > 0:
                vp.up(1)
            elif real_pos.y > 2:
                ppos.y -= 1
            else:
                move_was_blocked = True
        elif ch == curses.KEY_DOWN:
            last_move.y = 1
            if vp._top + vp._height < manor.size().y:
                vp.down(1)
            elif real_pos.y < manor.size().y - 1:
                ppos.y += 1
            else:
                move_was_blocked = True
        elif ch == curses.KEY_LEFT:
            last_move.x = -1
            if vp._left > 0:
                vp.left(1)
            elif real_pos.x > 2:
                ppos.x -= 1
            else:
                move_was_blocked = True
        elif ch == curses.KEY_RIGHT:
            last_move.x = 1
            if vp._left + vp._width < manor.size().x:
                vp.right(1)
            elif real_pos.x < manor.size().x - 1:
                ppos.x += 1
            else:
                move_was_blocked = True
        elif chr(ch) == 't':
            # Toggle between feature grid (true) and canvas view (false).
            print_features = not print_features
            did_move = False
        else:
            break

        if move_was_blocked:
            # Reset last_move.
            last_move = library.coord.Coord(0, 0)
            did_move = False

    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
