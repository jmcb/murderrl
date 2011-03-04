**********
Known bugs
**********

General or uncategorized
========================

Manor building
==============

* Doors are sometimes placed in a corner wall::

      #####
      #...#
      #...#
      ####+

* The corridor walls of the rooms in the leg attachment region (the rooms
  that had to have their size adjusted to fit the corridor) still claim to
  belong to the room on the other side of the room.

  Example::

      ########.########
      #......#.+......#
      #.porch+.#.guest#
      #......#.#..room#
      ########.########
               ^
               |- This wall (including the door!) claims to be part of the porch.

  If I move from the guest room to the corridor, the message area says:
  "You are currently in the porch." which, even ignoring the grammatical
  error is plainly wrong.

  This could be fixed by specialcasing all doors adjacent to a corridor as
  part of the corridor. (Due to the way corridors are placed, doors on one
  side of a corridor claim to be part of the corridor, doors on the other
  belong to the adjoining room. Only in this specialcase, neither is true.) 
  But that's only hiding the issue...
