#!/usr/bin/env python
"""
Attempt to create a "manor" akin to:

  ###############################################
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #.........#......#........#...........#.......#
  #########+####+######+###########+#####.......#
  #.......+......+......................+.......#
  #.......######+######+#.......#######+#########
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......#<<#....#.......#.......#
  #.......#......#......####....+.......#.......#
  #.......#......#......#..+....#.......#.......#
  ##########################....#################
                           ##++##

"""
import sys
sys.path.append("../")
import shape, coord, random, database

# Specific build styles:
ONE_CORRIDOR = "one-corridor"
L_CORRIDOR = "l-corridor"
Z_CORRIDOR = "z-corridor"

class Room (object):
    """
    Currently a builder-only representation of a room.
    """
    def __init__ (self, width=10, height=6, name="", start=None, stop=None):
        """
        Create a room.

        :``width``: The width of the room. *Default 10*.
        :``height``: The height of the room. *Default 6*.
        :``name``: The descriptive name of the room. ie, "Library". *Default ""*.
        :``start``: A coord denoting the top-left point of the room. *Default None*.
        :``stop``: A coord denoting the bottom-right point of the room. *Default None*.

        """
        self.width = width
        self.height = height
        self.name = name
        self.start = start
        self.stop = stop
    def as_shape (self):
        """
        Converts the room into a Shape object, by way of a Box.
        """
        return shape.Box(width=self.width, height=self.height, border=1, fill=".", border_fill="#")
    def __repr__ (self):
        return "<Room width=%s,height=%s,name=%s,start=%s,stop=%s>" % (self.width,self.height,self.name,self.start,self.stop)

def builder (style=ONE_CORRIDOR):
    """
    Attempts to build a manor based on the style provided. It returns
    ShapeCollection and a list of Room objects.

    :``style``: One of ``ONE_CORRIDOR``, ``L_CORRIDOR`` or ``Z_CORRIDOR``.
                Currently on ``ONE_CORRIDOR`` is supported. *Default
                ONE_CORRIDOR*.
    """
    room_names = database.rooms.copy()

    rooms = []

    if style == ONE_CORRIDOR:
        # Top row of rooms
        row1 = []
        # Corridor, then bottom row of rooms
        row2 = []

        # We start with the entrance hall and add rooms on either side of it
        # until we have a minimum of six and a maximum of ten
        entrance_hall = Room()

        left = 0
        right = 0

        row2.append(entrance_hall)

        while len(row2) <= 8:
            # If we have six rooms, one in three chance of not adding any more
            # rooms.
            if len(row2) > 5 and random.randint(1, 3) == 1:
                break

            name = room_names.random_pop()
            if not name:
                name = "UNKNOWN"

            new_room = Room(name=name)

            if left > right:
                row2.append(new_room)
                right += 1
            elif left < right:
                row2.insert(0, new_room)
                left += 1
            else:
                side = random.randint(-1, 0)
                if side == -1:
                    right += 1
                else:
                    left += 1
                row2.insert(side, new_room)

        while len(row1) < len(row2):
            name = room_names.random_pop()
            if not name:
                name = "UNKNOWN"
            new_room = Room(name=name)
            row1.append(new_room)

        # Now, adjust the rooms at either end to compensate for the corridor:
        # 1. We can adjust two rooms on the bottom level for height, 2 on the
        #    top for width.
        # 2. We can adjust one on the bottom and one on the top for height, and
        #    the opposites for width.
        # 3. We can adjust two rooms on the top level for height, 2 on the
        #    bottom for width.
        adjust_bottom = random.randint(0, 2)
        if adjust_bottom == 2:
            row2[0].height += 2
            row2[-1].height += 2
            row1[0].width += 1
            row1[1].width -= 1
            row1[-1].width += 1
            row1[-2].width -= 1
        elif adjust_bottom == 1:
            side_adjusted = random.randint(-1, 0)
            side_not_adjusted = -side_adjusted-1
            row2[side_adjusted].height += 2
            row1[side_not_adjusted].height += 2

            row2[side_not_adjusted].width += 1
            if side_not_adjusted == -1:
                row2[-2].width -= 1
            else:
                row2[1].width -= 1

            row1[side_adjusted].width += 1
            if side_adjusted == -1:
                row2[-2].width -= 1
            else:
                row2[1].width -= 1
        elif adjust_bottom == 0:
            row1[0].height += 2
            row1[-1].height += 2
            row2[0].width += 1
            row2[1].width -= 1
            row2[-1].width += 1
            row2[-2].width -= 1

        # Now, start drawing it! YAY!
        first_room = row1[0].as_shape()
        second_room = row1[1].as_shape()
        collection = shape.adjoin(first_room, second_room, overlap=1, collection=True)
        for room in row1[1:]:
            collection = shape.adjoin(collection, room.as_shape(), overlap=1, collection=True)

        return collection

    else:
        return shape.ShapeCollection(), rooms

if __name__=="__main__":
    builder()
