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
from library.feature import *

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
    # base_manor = builder.manor.build_L()
    base_manor = builder.manor.build_random()

    # Translate rooms and corridors into wall and floor features.
    base_manor.init_features()
    # Add doors along corridors.
    base_manor.add_doors()
    # Add doors along corridors, and windows.
    base_manor.add_windows()
    # Combine the room shapes into a canvas.
    manor = base_manor.combine()

    # Draw features on canvas.
    for pos in library.coord.RectangleIterator(manor.size()):
        feat = base_manor.get_feature(pos)
        if feat != NOTHING and feat != WALL and feat != FLOOR:
            manor.__setitem__(pos, feat.glyph())

    # Initialise the view port.
    vp = library.viewport.ViewPort(buffer=manor,
                                   width =min(manor.size().width, 70),
                                   height=min(manor.size().height, 20))

    # Initially place the player in the centre of the entrance hall.
    ehall = base_manor.get_room(base_manor.entrance_hall)
    real_pos = library.coord.Coord(ehall.pos().x + ehall.size().x/2, ehall.pos().y + ehall.size().y/2)

    # Initialise a couple of other variables.
    last_move = library.coord.Coord(0, 0) # the last step taken by the player
    move_was_blocked = False   # bumped into a wall
    did_move         = True    # actually took a step
    print_features   = False   # draw manor via the feature grid
    tried_move_feat  = NOTHING # The feature the player tried to move on.
    while True:
        screen.clear(" ")

        # The currently visible section of the viewport, centered on the player.
        vp.centre(real_pos, manor.size())
        sect = vp.sect()

        # Depending on the current toggle state (toggle key 't'), either draw
        # the manor via the feature grid, or via the shape canvas.
        if print_features:
            for coord in library.coord.RectangleIterator(sect.size()):
                if coord >= base_manor.features.size():
                    continue
                real_coord = coord + library.coord.Coord(vp._left, vp._top)
                char = base_manor.features.__getitem__(real_coord).glyph()
                screen.put(char, coord+1)
        else:
            for coord, char in sect:
                if char == None:
                    char = " "
                screen.put(char, coord+1)

        canvas_pos = library.coord.Coord(real_pos.x - vp._left, real_pos.y - vp._top)
        # Draw the player.
        screen.put("@", canvas_pos + 1)

        if move_was_blocked:
            put_text("Ouch! You bump into a %s!" % tried_move_feat.name(), library.coord.Coord(0, 22))
        elif not did_move:
            mode = "canvas view"
            if print_features:
                mode = "feature grid"
            put_text("Switched to %s." % mode, library.coord.Coord(0, 22))
        elif base_manor.features.__getitem__(real_pos) == CLOSED_DOOR:
            put_text("You see here a door.", library.coord.Coord(0, 22))

        ## Debugging information.

        # Get the current room/corridor id.
        id = base_manor.get_corridor_index(real_pos + 1)
        type = "corridor"
        if id == None:
            id   = base_manor.get_room_index(real_pos +  1)
            type = "room"
        room_desc = base_manor.get_roomprop(id)
        put_text("Sect size : %s, Start coord: %s, Stop coord: %s, %s" % (sect.size(), library.coord.Coord(vp._left, vp._top), library.coord.Coord(vp._left + vp._width, vp._top + vp._height), room_desc), library.coord.Coord(0, 23))

        put_text("Manor size: %s, Player coord: %s, last_move: %s, %s id: %s" % (manor.size(), real_pos + 1, last_move, type, id), library.coord.Coord(0, 24))

        # Get a key.
        ch = screen.get(block=True)

        # Move the player (@) via the arrow keys.
        # If we haven't reached the manor boundaries yet, scroll in that direction.
        # Otherwise, take a step unless it would make us leave the manor.

        # Reinitialise the relevant variables.
        last_move        = library.coord.Coord(0, 0)
        move_was_blocked = False
        did_move         = True
        tried_move_feat  = NOTHING
        if ch == curses.KEY_UP:
            last_move.y = -1
            next_pos = real_pos + last_move
            if next_pos.y < 0:
                move_was_blocked = True
                continue
            tried_move_feat = base_manor.get_feature(next_pos)
            if not tried_move_feat.traversable():
                move_was_blocked = True
            else:
                real_pos.y -= 1
        elif ch == curses.KEY_DOWN:
            last_move.y = 1
            next_pos = real_pos + last_move
            if next_pos.y >= manor.size().y:
                move_was_blocked = True
                continue
            tried_move_feat = base_manor.get_feature(next_pos)
            if not tried_move_feat.traversable():
                move_was_blocked = True
            else:
                real_pos.y += 1
        elif ch == curses.KEY_LEFT:
            last_move.x = -1
            next_pos = real_pos + last_move
            if next_pos.x < 0:
                move_was_blocked = True
                continue
            tried_move_feat = base_manor.get_feature(next_pos)
            if not tried_move_feat.traversable():
                move_was_blocked = True
            else:
                real_pos.x -= 1
        elif ch == curses.KEY_RIGHT:
            last_move.x = 1
            next_pos = real_pos + last_move
            if next_pos.x >= manor.size().x:
                move_was_blocked = True
                continue
            tried_move_feat = base_manor.get_feature(next_pos)
            if not tried_move_feat.traversable():
                move_was_blocked = True
            else:
                real_pos.x += 1
        elif chr(ch) == 'd':
            # Describe current room.
            room = base_manor.get_roomprop(id)
            room.describe()
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
