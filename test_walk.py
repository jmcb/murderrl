#!/usr/bin/env python
"""
A demo of a ghostly @ walking through walls in an unfurnished manor. :P
"""

import curses

import builder.manor
import library.viewport, library.coord
import interface.console

screen = interface.console.select()

def put_text (text, spot):
    for ind, char in enumerate(text):
        screen.put(char, library.coord.Coord(spot.x+ind, spot.y))

def main ():
    screen.init()

    base_manor = builder.manor.build_random()
    manor = base_manor.combine()

    print "Rooms:"
    base_manor.print_rooms()
    print "#Legs: ", base_manor.count_legs()
    for i in base_manor.legs:
        print i
    print "Corridors:"
    base_manor.print_corridors()

    vp = library.viewport.ViewPort(buffer=manor,
                                   width =min(manor.size().width, 70),
                                   height=min(manor.size().width, 20))

    # player (@) position in the viewport
    ppos      = library.coord.Coord(35, 10)
    # the last step taken by the player
    last_move = library.coord.Coord(0, 0)
    # initial placement
    placement = True
    while True:
        screen.clear(" ")

        sect = vp.sect()

        # The real player position in the manor.
        real_pos = library.coord.Coord(vp._left + ppos.x + 1, vp._top + ppos.y + 1)
        for coord, char in sect:
            if char == None:
                char = " "
                # Don't place the player outside the manor.
                # Initially place him elsewhere, later disallow such movements.
                if (coord == ppos):
                    if placement:
                        ppos.x += 2
                    else:
                        ppos = ppos - last_move
                        char = "X"

            screen.put(char, coord+1)

        placement = False
        screen.put("@", ppos + 1)
        # Debugging information.
        put_text("Sect size : %s, Start coord: %s, Stop coord: %s" % (sect.size(), library.coord.Coord(vp._left, vp._top), library.coord.Coord(vp._left + vp._width, vp._top + vp._height)), library.coord.Coord(0, 23))

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
        last_move = library.coord.Coord(0, 0)
        move_was_blocked = False
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
        else:
            break

        if move_was_blocked:
            # reset last_move
            last_move = library.coord.Coord(0, 0)

    screen.deinit()

if __name__=="__main__":
    screen.wrapper(main)
