*****
To do
*****

General or uncategorized
========================

1. Abstraction layer between Shape and the actual manor: background (floor or
   wall), middle ground (furniture?), foreground (player or other suspects or
   characters).
2. A* or similar pathfinding mechanism.
3. Random character movement.
4. Time passage implementation.
5. Glyph definitions.

Suspect generation
==================

1. Store clues and so-on in a database.

Manor building
==============

1. Extend builder's leg generation to support multiple configurations.
2. Provide "corridor" iterator that returns the length of the manor corridor.
3. Find a good algorithm for compartmentalising the house into "domestic" and
   "utility" sections.
4. Randomise room sizes; some rooms should be smaller than others.
5. Finish implementing the ManorCollection.
6. Implement "join" function for ShapeCollections: combine two overlapping
   shapes into one shape that replaces both indexes.
7. Write ShapeCollection::place_on(collection, offset). Offsets collection and
   appends its contents to the target collection.
8. Write ShapeCollection::draw_on(shape, offset).

User interface
==============

1. Implement a view-port for urwid that translates a Shape into a TextWidget.

Databases
=========

1. Correct get_database, etc, to tree dot-point notation accordingly.
2. Default spec for databases.
3. Allow for combinations of "$<var>" and "$<digit>" in specifications, which
   requires dumping tuple support but I don't see this as issueous.
4. Code "%alias <short> <var name>" and its support.

Recently completed
==================

1. Implement databases to allow for subdirectories.
