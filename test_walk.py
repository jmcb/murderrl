#!/usr/bin/env python
"""
A demo of our @ detective walking through an otherwise empty manor. :P
Toggle canvas vs. feature view with 't'. (Should be identical.)
"""

import curses

import builder.manor
from library import viewport, coord
import interface.console
from interface.features import *
from interface.output import *
from library.feature import *

screen = interface.console.select()

def is_traversable (feature_grid, pos):
    return feature_grid.__getitem__(pos).traversable()

def get_command_help ():
    help  = "Command help\n\n"
    help += "Use the arrow keys for movement.\n\n"
    help += "d: describe current room\n"
    help += "h: display this screen\n"
    help += "t: toggle between canvas view (default) and feature grid\n\n"
    help += "Any other key exits the program."
    return help

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
    for pos in coord.RectangleIterator(manor.size()):
        feat = base_manor.get_feature(pos)
        if feat != NOTHING and feat != WALL and feat != FLOOR:
            manor.__setitem__(pos, feat.glyph())

    # Initialise the view port.
    vp = viewport.ViewPort(buffer=manor,
                           width =min(manor.size().width, 70),
                           height=min(manor.size().height, 20))

    # Initially place the player in the centre of the entrance hall.
    ehall = base_manor.get_room(base_manor.entrance_hall)
    real_pos = coord.Coord(ehall.pos().x + ehall.size().x/2, ehall.pos().y + ehall.size().y/2)

    # Initialise a couple of other variables.
    last_move = coord.Coord(0, 0) # the last step taken by the player
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
            for pos in coord.RectangleIterator(sect.size()):
                if pos >= base_manor.features.size():
                    continue
                real_coord = pos + coord.Coord(vp._left, vp._top)
                char = base_manor.features.__getitem__(real_coord).glyph()
                screen.put(char,pos+1)
        else:
            for pos, char in sect:
                if char == None:
                    char = " "
                screen.put(char, pos+1)

        canvas_pos = coord.Coord(real_pos.x - vp._left, real_pos.y - vp._top)
        # Draw the player.
        screen.put("@", canvas_pos + 1)

        if move_was_blocked:
            print_line("Ouch! You bump into a %s!" % tried_move_feat.name(), coord.Coord(0, 22))
        elif not did_move:
            mode = "canvas view"
            if print_features:
                mode = "feature grid"
            print_line("Switched to %s." % mode, coord.Coord(0, 22))
        elif base_manor.features.__getitem__(real_pos) == CLOSED_DOOR:
            print_line("You see here a door.", coord.Coord(0, 22))

        ## Debugging information.

        # Get the current room/corridor id.
        id = base_manor.get_corridor_index(real_pos + 1)
        type = "corridor"
        if id == None:
            id   = base_manor.get_room_index(real_pos +  1)
            type = "room"
        room_desc = base_manor.get_roomprop(id)
        print_line("Sect size : %s, Start coord: %s, Stop coord: %s, %s" % (sect.size(), coord.Coord(vp._left, vp._top), coord.Coord(vp._left + vp._width, vp._top + vp._height), room_desc), coord.Coord(0, 23))

        print_line("Manor size: %s, Player coord: %s, last_move: %s, %s id: %s" % (manor.size(), real_pos + 1, last_move, type, id), coord.Coord(0, 24))

        # Get a key.
        ch = screen.get(block=True)

        # Move the player (@) via the arrow keys.
        # If we haven't reached the manor boundaries yet, scroll in that direction.
        # Otherwise, take a step unless it would make us leave the manor.

        # Reinitialise the relevant variables.
        last_move        = coord.Coord(0, 0)
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
        elif chr(ch) == 'h':
            # Print command help.
            print_screen(get_command_help())
        elif chr(ch) == 't':
            # Toggle between feature grid (true) and canvas view (false).
            print_features = not print_features
            did_move = False
        else:
            break

        if move_was_blocked:
            # Reset last_move.
            last_move = coord.Coord(0, 0)
            did_move  = False

    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
