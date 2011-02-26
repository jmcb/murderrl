#!/usr/bin/env python
"""
A demo of our @ detective walking through an otherwise empty manor. :P
Toggle canvas vs. feature view with 't'. (Should be identical.)
"""

import curses

import builder.manor
from library import viewport
from library.coord import *
from library.feature import *
import interface.console
from interface.features import *
from interface.output import *
from suspects.randname import *

screen = interface.console.select()

def feature_is_door (feat):
    return feat == OPEN_DOOR or feat == CLOSED_DOOR

# The message line.
# Following lines may get used for debugging output.
MSG_LINE  = 22
MSG_START = coord.Coord(0, MSG_LINE)

class Game (object):
    """
    The module to handle the main game loop.
    """
    def __init__ (self):
        """
        Initialise the manor, viewport and other objects and parameters.
        """
        # First, build the manor.
        # self.base_manor = builder.manor.base_builder()
        # self.base_manor = builder.manor.build_L()
        self.base_manor = builder.manor.build_random()

        # Translate rooms and corridors into wall and floor features.
        self.base_manor.init_features()
        # Add doors along corridors.
        self.base_manor.add_doors()
        # Add doors along corridors, and windows.
        self.base_manor.add_windows()
        # Combine the room shapes into a canvas.
        self.canvas = self.base_manor.combine()

        # Draw features on canvas.
        for pos in coord.RectangleIterator(self.canvas.size()):
            feat = self.base_manor.get_feature(pos)
            if feat != NOTHING and feat != WALL and feat != FLOOR:
                self.canvas.__setitem__(pos, feat.glyph())

        # Initialise the view port.
        self.vp = viewport.ViewPort(buffer=self.canvas,
                                    width =min(self.canvas.size().width, 70),
                                    height=min(self.canvas.size().height, 20))

        # Initialise a couple of other variables.
        self.initialise_parameters()

    def initialise_parameters (self):
        """
        Initialise the simple parameters.
        """
        # Initially place the player in the centre of the entrance hall.
        ehall = self.base_manor.get_room(self.base_manor.entrance_hall)
        self.player_pos = coord.Coord(ehall.pos().x + ehall.size().x/2, ehall.pos().y + ehall.size().y/2)

        self.game_start       = True    # Game just started.
        self.debugging        = False   # debugging mode
        self.last_move        = DIR_NOWHERE # the last step taken by the player
        self.move_was_blocked = False   # bumped into a wall
        self.did_move         = True    # actually took a step
        self.tried_move_feat  = NOTHING # The feature the player tried to move on.
        self.dir_running      = DIR_NOWHERE # Direction we are running (if any).
        self.was_running      = False   # Running just stopped.

    def get_welcome_message (self):
        """
        Returns the message that is printed at game start.
        """
        return "Welcome to %s! To view the list of commands, press 'h'." % get_random_manor_name()

    def draw_feature_grid (self):
        """
        Draws the feature grid onto the screen. (Only in debug mode.)
        """
        for pos in coord.RectangleIterator(self.sect.size()):
            if pos >= self.base_manor.features.size():
                continue
            real_coord = pos + coord.Coord(self.vp._left, self.vp._top)
            char = self.base_manor.features.__getitem__(real_coord).glyph()
            screen.put(char,pos+1)

    def draw_canvas (self):
        """
        Draws the section of the viewport that's currently visible onto the screen.
        """
        for pos, char in self.sect:
            if char == None:
                char = " "
            screen.put(char, pos+1)

    def draw_viewport (self):
        """
        Draws the game map, including the player glyph, onto the screen.
        """
        # The currently visible section of the viewport, centered on the player.
        self.vp.centre(self.player_pos, self.canvas.size())
        self.sect = self.vp.sect()

        # Depending on the current toggle state (toggle key 't'), either draw
        # the manor via the feature grid (debugging = true), or via the shape canvas.
        if self.debugging:
            self.draw_feature_grid()
        else:
            self.draw_canvas()

        # Draw the player.
        canvas_pos = coord.Coord(self.player_pos.x - self.vp._left, self.player_pos.y - self.vp._top)
        screen.put("@", canvas_pos + 1)

    def get_current_room (self):
        """
        Returns the RoomProps object matching the player's current position.
        """
        # Get the current room/corridor id.
        id = self.base_manor.get_corridor_index(self.player_pos + 1)
        type = "corridor"
        if id == None:
            id   = self.base_manor.get_room_index(self.player_pos + 1)
            type = "room"
        return self.base_manor.get_roomprop(id)

    def print_debugging_messages (self):
        """
        Prints a variety of parameters in the message area. (Only in debug mode.)
        """
        # Get the current room/corridor id.
        id = self.base_manor.get_corridor_index(self.player_pos + 1)
        type = "corridor"
        if id == None:
            id   = self.base_manor.get_room_index(self.player_pos + 1)
            type = "room"
        room_desc = self.base_manor.get_roomprop(id)

        print_line("Sect size : %s, Start coord: %s, Stop coord: %s, %s" % (self.sect.size(), coord.Coord(self.vp._left, self.vp._top), coord.Coord(self.vp._left + self.vp._width, self.vp._top + self.vp._height), room_desc), coord.Coord(0, MSG_LINE+1))

        print_line("Manor size: %s, Player coord: %s, last_move: %s, %s id: %s" % (self.canvas.size(), self.player_pos + 1, self.last_move, type, id), coord.Coord(0, MSG_LINE+2))

    def draw_messages (self):
        """
        Writes game messages into the message area.
        """
        if self.game_start:
            print_line(self.get_welcome_message(), MSG_START)
            self.game_start = False
        elif self.move_was_blocked:
            print_line("Ouch! You bump into a %s!" % self.tried_move_feat.name(), MSG_START)
        elif not self.did_move and not self.was_running:
            mode = "canvas view"
            if self.debugging:
                mode = "debug mode"
            print_line("Switched to %s." % mode, MSG_START)
        elif feature_is_door(self.base_manor.get_feature(self.player_pos)):
            print_line("You see here a door.", MSG_START)

        if self.debugging:
            # Debugging information.
            self.print_debugging_messages()
        else:
            print_line("You are currently in the %s." % self.get_current_room(), coord.Coord(0, MSG_LINE+1))

    def update_screen (self):
        """
        Updates game map and message area.
        """
        # Note: Currently the screen gets cleared completely. Splitting that
        #       for map/message area could be useful. (jpeg)
        screen.clear(" ")
        self.draw_viewport()
        self.draw_messages()

    def cmd_describe_room (self, pos = None):
        """
        Describes the room a given position belongs to.

        :``pos``: A coordinate in the manor. If none, the player position is used. 
                  *Default: none*.
        """
        if pos == None:
            pos = self.player_pos

        # Describe current room.
        id = self.base_manor.get_corridor_index(pos + 1)
        if id == None:
            id = self.base_manor.get_room_index(pos + 1)
        room = self.base_manor.get_roomprop(id)
        room.describe()

    def get_command_help (self):
        """
        Returns a string of command keys and their explanation.
        """
        help  = "Command help\n\n"
        help += "Use the arrow keys for movement.\n\n"
        help += "r followed by a direction: start running in that direction\n\n"
        help += "d: describe current room\n"
        help += "h: display this screen\n"
        help += "t: toggle between canvas view (default) and feature grid\n\n"
        help += "Any other key exits the program."
        return help

    def reinit_movement_parameters (self):
        """
        Reinitialises parameters pertaining to movement to their default values.
        """
        self.last_move        = DIR_NOWHERE
        self.move_was_blocked = False
        self.did_move         = True
        self.tried_move_feat  = NOTHING
        self.was_running      = (self.dir_running != DIR_NOWHERE)

    def handle_movement_keys (self, ch):
        """
        Checks whether a given keypress matches any of the movement keys
        and, if so, returns the matching directional coordinate.

        :``ch``: The key pressed by the player. *Required*.
        """
        if ch == curses.KEY_UP:
            return DIR_NORTH
        if ch == curses.KEY_DOWN:
            return DIR_SOUTH
        if ch == curses.KEY_LEFT:
            return DIR_WEST
        if ch == curses.KEY_RIGHT:
            return DIR_EAST

        return DIR_NOWHERE

    def cmd_start_running (self):
        """
        Prompts for a direction key and starts moving the player in that
        direction until we run into an obstacle or reach an adjacent door.
        """
        ch = screen.get(block=True)
        self.dir_running = self.handle_movement_keys(ch)
        self.was_running = True
        if self.dir_running != DIR_NOWHERE:
            self.last_move = self.dir_running
            self.did_move  = True

    def handle_movement_commands (self):
        """
        Check whether the planned move is valid. If so, actually move the
        player. Otherwise, change a few parameters.
        """
        curr_pos = self.player_pos
        next_pos = curr_pos + self.last_move
        if (next_pos.x < 0 or next_pos.y < 0
        or next_pos.x >= self.base_manor.size().x or next_pos.y >= self.base_manor.size().y):
            self.move_was_blocked = True
        else:
            self.tried_move_feat = self.base_manor.get_feature(next_pos)
            if not self.tried_move_feat.traversable():
                self.move_was_blocked = True
            else:
                curr_pos += self.last_move
                if self.dir_running != DIR_NOWHERE:
                    # check whether we need to stop
                    if feature_is_door(self.base_manor.get_feature(curr_pos)):
                        self.dir_running = DIR_NOWHERE
                    else:
                        in_corr = (self.base_manor.get_corridor_index(curr_pos + 1) != None)
                        dirs = (DIR_NORTH, DIR_SOUTH, DIR_WEST, DIR_EAST)
                        for d in dirs:
                            if d == self.dir_running or DIR_NOWHERE - d == self.dir_running:
                                continue
                            if (in_corr and self.base_manor.get_feature(curr_pos + d) == FLOOR
                            or feature_is_door(self.base_manor.get_feature(curr_pos + d))):
                                self.dir_running = DIR_NOWHERE
                                break

        if self.move_was_blocked:
            # Reset last_move.
            self.last_move = DIR_NOWHERE
            self.did_move  = False
            if self.was_running:
                # No running into wall messages.
                self.move_was_blocked = False
                self.dir_running      = DIR_NOWHERE

    def handle_commands (self):
        """
        Wait for a keypress and execute the corresponding action.
        Returns true if the game loop should continue, and false if we
        want to exit the loop.
        """
        curr_pos = self.player_pos

        # Get a key.
        if self.dir_running == DIR_NOWHERE:
            ch = screen.get(block=True)

            if ch > 0 and ch <= 256:
                self.did_move = False
                if chr(ch) == 'd':
                    self.cmd_describe_room()
                elif chr(ch) == 'h':
                    # Print command help.
                    print_screen(self.get_command_help())
                elif chr(ch) == 'r':
                    self.cmd_start_running()
                elif chr(ch) == 't':
                    # Toggle debugging mode on and off.
                    self.debugging = not self.debugging
                else: # exit the game
                    return False
            else:
                # Move the player (@) via the arrow keys.
                # If we haven't reached the manor boundaries yet, scroll in that direction.
                # Otherwise, take a step unless it would make us leave the manor.
                self.last_move = self.handle_movement_keys(ch)
        else:
            self.last_move = self.dir_running

        # Actually move the player, if the new position is valid.
        if self.last_move != DIR_NOWHERE:
            self.handle_movement_commands()

        return True

    def do_loop (self):
        """
        Run the actual game loop. Returns if we encounter an invalid keypress.
        """
        while True:
            if self.dir_running == DIR_NOWHERE:
                self.update_screen()

            # Reinitialise the relevant variables.
            self.reinit_movement_parameters()

            if not self.handle_commands():
                return

def main ():
    screen.init()
    game = Game()
    game.do_loop()
    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
