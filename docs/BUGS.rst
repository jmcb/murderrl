**********
Known bugs
**********

General or uncategorized
========================

Manor building
==============

* The same door is counted twice for corridor cross section.

  ####.#...
  ####.#.A
  ####.#...
  ....,'...
  #########

  In the above image, room A has a door leading to a cross section between
  the main and the north east corridor. In this special case, both
  corridors are considered as adjoining to A, meaning A's room description
  will include a mention of
    "doors leading to the main corridor and the north east corridor"
  which is confusing as there's only one door.

  One solution to fix this is to decrease the length of the non-main
  corridors by 1 (and adjust the starting position for the south corridors),
  so overlapping corridors no longer exist.

* Some of the neighbour rooms don't work well together.

  This is more of FR, but sometimes two adjacent rooms really don't work
  well together. This is most apparent if a bedroom is adjoining another
  (passage) room, and especially if said room is part of the utility
  section. Utility rooms as passage rooms to domestic rooms in general
  strike me as odd. I once had a string of connected rooms leading from
  pantry > smoking room > kitchen > corridor. I liked having the pantry
  close to the kitchen, but the smoking room in-between was really out of
  place. Smoked food works somewhat differently... ;)
