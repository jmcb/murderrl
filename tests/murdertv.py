#!/usr/bin/env python
"""
Play the actual game. Let the sleuthing begin!
"""

import interface.console
from game import mainloop
from builder import builder, manor
from library.coord import *
from library.random_util import *
from suspects import person

screen = interface.console.select()

def murderer_flees (game, sid):
    s   = game.suspect_list.get_murderer()
    rid = s.alibi.rid
    game.set_suspect_path(sid, rid)

def init_suspect_positions (game):
    sl    = game.suspect_list
    manor = game.base_manor
    for sid in xrange(len(sl.suspects)):
        if sid == sl.victim:
            continue

        s = sl.get_suspect(sid)
        s.path = []
        if sid == sl.murderer:
            candidates = []
            for c in AdjacencyIterator(sl.get_victim().pos):
                if manor.get_feature(c).traversable():
                    candidates.append(c)
            if len(candidates) > 0:
                s.pos = random.choice(candidates)
                murderer_flees(game, sid)
                continue

        alibi = s.alibi
        if alibi == None:
            rid = random.choice(manor.rooms)
        else:
            rid = s.alibi.rid

        room  = manor.get_room(rid)
        start = room.pos() + 1
        stop  = room.pos() + room.size() - 2

        while True:
            s.pos = Coord(random.randint(start.x, stop.x), random.randint(start.y, stop.y))
            if manor.get_feature(s.pos).traversable():
                break

        # The murderer is trying to leave as quickly as possible.
        if sid == sl.murderer:
            murderer_flees(game, sid)
            continue

        if s.alibi == None:
            rid = None
        else:
            rid = s.alibi.rid
        rp  = game.base_manor.room_props[rid]
        if sid in rp.owners:
            if s.gender == 'f':
                pronoun = "her"
            else:
                pronoun = "his"
            print "%s is already in %s bedroom." % (s.get_name(), pronoun)
            # Suspect in their own bedroom -> they won't be leaving for a while.
            s.duration = 100

def main ():
    screen.init()
    game = mainloop.Game(type='B')
    sl   = game.suspect_list
    m    = game.base_manor
    murder_room = sl.get_victim().alibi.rid
    print "Murder room: %s" % m.room_props[murder_room].name
    body_found  = False

    while True:
        init_suspect_positions(game)
        game.turns = 780
        do_pause   = True
        for i in xrange(159):
            game.update_screen()
            ch = screen.get(block=do_pause)
            if ch > 0 and ch <= 256:
                if chr(ch) == 'p':
                    do_pause = True
                elif chr(ch) == 'c':
                    do_pause = False
                elif chr(ch) == 'q':
                    break
            else:
                game.init_command_parameters()
                game.last_move = game.handle_movement_keys(ch)
                if game.last_move != DIR_NOWHERE:
                    game.handle_movement_commands()

            game.move_suspect(sl.murderer)
            game.handle_time()

            if not body_found:
                for sid in xrange(len(sl.suspects)):
                    if sid == sl.victim:
                        continue
                    if m.get_room_index(sl.get_suspect(sid).pos) == murder_room:
                        if sid == sl.murderer and game.turns < 800:
                            continue
                        print "-------------------------------"
                        print "%s discovers the body!" % sl.get_suspect(sid).get_name()
                        print "-------------------------------"
                        body_found = True
                        break

        game.message = "Repeat? Everything but (y)es, (c)ontinue, (r)epeat will stop the game."
        game.update_screen()
        ch = screen.get(block=True)
        if ch > 0 and ch <= 256:
            if chr(ch) == 'c' or chr(ch) == 'r' or chr(ch) == 'y':
                continue
        break

    screen.deinit()

if __name__ == "__main__":
    screen.wrapper(main)
