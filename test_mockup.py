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
from suspects.randname import *

screen = interface.console.select()

def is_traversable (feature_grid, pos):
    return feature_grid.__getitem__(pos).traversable()

def get_command_help ():
    help  = "Command help\n\n"
    help += "Use the arrow keys for movement.\n\n"
    help += "r followed by a direction: start running in that direction\n\n"
    help += "d: describe current room\n"
    help += "h: display this screen\n"
    help += "t: toggle between canvas view (default) and feature grid\n\n"
    help += "Any other key exits the program."
    return help

# Define directions.
DIR_NORTH   = coord.Coord(0, -1)
DIR_SOUTH   = coord.Coord(0, +1)
DIR_WEST    = coord.Coord(-1, 0)
DIR_EAST    = coord.Coord(+1, 0)
DIR_NOWHERE = coord.Coord(0, 0)

def handle_movement_keys (ch):
    if ch == curses.KEY_UP:
        return DIR_NORTH
    if ch == curses.KEY_DOWN:
        return DIR_SOUTH
    if ch == curses.KEY_LEFT:
        return DIR_WEST
    if ch == curses.KEY_RIGHT:
        return DIR_EAST

    return DIR_NOWHERE

def get_welcome_message ():
    return "Welcome to %s! To view the list of commands, press 'h'." % get_random_manor_name()

# The message line.
# Following lines may get used for debugging output.
MSG_LINE = 22

def feature_is_door (feat):
    return feat == OPEN_DOOR or feat == CLOSED_DOOR

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
    last_move        = DIR_NOWHERE # the last step taken by the player
    game_start       = True    # Game just started.
    move_was_blocked = False   # bumped into a wall
    did_move         = True    # actually took a step
    debugging        = False   # debugging mode
    tried_move_feat  = NOTHING # The feature the player tried to move on.
    dir_running      = DIR_NOWHERE # Direction we are running (if any).
    while True:
        if dir_running == DIR_NOWHERE:
            screen.clear(" ")

            # The currently visible section of the viewport, centered on the player.
            vp.centre(real_pos, manor.size())
            sect = vp.sect()

            # Depending on the current toggle state (toggle key 't'), either draw
            # the manor via the feature grid (debugging = true), or via the shape canvas.
            if debugging:
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

            if game_start:
                print_line(get_welcome_message(), coord.Coord(0, MSG_LINE))
                game_start = False
            elif move_was_blocked:
                print_line("Ouch! You bump into a %s!" % tried_move_feat.name(), coord.Coord(0, MSG_LINE))
            elif not did_move:
                mode = "canvas view"
                if debugging:
                    mode = "debug mode"
                print_line("Switched to %s." % mode, coord.Coord(0, MSG_LINE))
            elif feature_is_door(base_manor.get_feature(real_pos)):
                print_line("You see here a door.", coord.Coord(0, MSG_LINE))

            ## Debugging information.

            # Get the current room/corridor id.
            id = base_manor.get_corridor_index(real_pos + 1)
            type = "corridor"
            if id == None:
                id   = base_manor.get_room_index(real_pos +  1)
                type = "room"
            room_desc = base_manor.get_roomprop(id)
            if debugging:
                print_line("Sect size : %s, Start coord: %s, Stop coord: %s, %s" % (sect.size(), coord.Coord(vp._left, vp._top), coord.Coord(vp.    _left + vp._width, vp._top + vp._height), room_desc), coord.Coord(0, MSG_LINE+1))

                print_line("Manor size: %s, Player coord: %s, last_move: %s, %s id: %s" % (manor.size(), real_pos + 1, last_move, type, id), coord.Coord(0, MSG_LINE+2))
            else:
                print_line("You are currently in the %s." % room_desc, coord.Coord(0, MSG_LINE+1))

        # Reinitialise the relevant variables.
        last_move        = DIR_NOWHERE
        move_was_blocked = False
        did_move         = True
        tried_move_feat  = NOTHING

        # Get a key.
        if dir_running == DIR_NOWHERE:
            ch = screen.get(block=True)

            if ch > 0 and ch <= 256:
                if chr(ch) == 'd':
                    # Describe current room.
                    room = base_manor.get_roomprop(id)
                    room.describe()
                elif chr(ch) == 'h':
                    # Print command help.
                    print_screen(get_command_help())
                    did_move = False
                elif chr(ch) == 'r':
                    # Start running into a given direction.
                    ch = screen.get(block=True)
                    dir_running = handle_movement_keys(ch)
                    if dir_running == DIR_NOWHERE:
                        did_move = False
                    else:
                        last_move = dir_running
                elif chr(ch) == 't':
                    # Toggle debugging mode on and off.
                    debugging = not debugging
                    did_move  = False
                else:
                    break
            else:
                # Move the player (@) via the arrow keys.
                # If we haven't reached the manor boundaries yet, scroll in that direction.
                # Otherwise, take a step unless it would make us leave the manor.
                last_move = handle_movement_keys(ch)
        else:
            last_move = dir_running

        if last_move != DIR_NOWHERE:
            next_pos = real_pos + last_move
            if (next_pos.x < 0 or next_pos.y < 0
            or next_pos.x >= base_manor.size().x or next_pos.y >= base_manor.size().y):
                move_was_blocked = True
            else:
                tried_move_feat = base_manor.get_feature(next_pos)
                if not tried_move_feat.traversable():
                    move_was_blocked = True
                else:
                    real_pos += last_move
                    if dir_running != DIR_NOWHERE:
                        # check whether we need to stop
                        if feature_is_door(base_manor.get_feature(real_pos)):
                            dir_running = DIR_NOWHERE
                        else:
                            in_corr = (base_manor.get_corridor_index(real_pos + 1) != None)
                            dirs = (DIR_NORTH, DIR_SOUTH, DIR_WEST, DIR_EAST)
                            for d in dirs:
                                if d == dir_running or DIR_NOWHERE - d == dir_running:
                                    continue
                                if (in_corr and base_manor.get_feature(real_pos + d) == FLOOR
                                or feature_is_door(base_manor.get_feature(real_pos + d))):
                                    dir_running = DIR_NOWHERE
                                    break

            if move_was_blocked:
                # Reset last_move.
                last_move = DIR_NOWHERE
                did_move  = False
                dir_running = DIR_NOWHERE

    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
