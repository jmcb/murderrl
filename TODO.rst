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

1. Extend the builder to generate Z, N, T, H, U, O, C, etc, interfaces.
2. Implement coord-access to ShapeCollections if that coord falls within a
   contained shape.
3. Provide translation layer from iterators in Shapes in ShapeCollections to an
   iterator of ShapeCollection.
4. Provide "corridor" iterator that returns the length of the manor corridor.
5. Find a good algorithm for compartmentalising the house into "domestic" and
   "utility" sections.
6. Randomise room sizes; some rooms should be smaller than others.
7. Casting of AutoShape into Shapes.

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
