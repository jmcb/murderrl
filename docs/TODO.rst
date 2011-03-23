*****
To do
*****

General or uncategorized
========================

1. Abstraction layer between Shape and the actual manor: background (floor or
   wall), middle ground (furniture?), foreground (player or other suspects or
   characters).
2. Random character movement.
3. Time passage implementation.
4. Glyph definitions.

Suspect generation
==================

1. Store clues and so-on in a database.

Manor building
==============

1. Extend builder's leg generation to support multiple configurations.
   > Looks good to me, though the occasional O-, C- or T-layout would be
   > kinda nice. In theory, it shouldn't be too difficult to connect a
   > single leg with 2 base builders. The problem is that the manor
   > currently assumes that the base builder's corridor is the main corridor
   > and that there can only be one main corridor.
2. Provide "corridor" iterator that returns the length of the manor corridor.
3. Randomise room sizes; some rooms should be smaller than others.
   > Much better now than it used to be, though there's still room for
   > improvement.
4. Finish implementing the ManorCollection.
   > Meaning what, precisely?
5. Implement "join" function for ShapeCollections: combine two overlapping
   shapes into one shape that replaces both indexes.
   > If the resulting shape would still be rectangular, this could be
   > occasionally useful to merge a leg room and a base manor room.
   > If the shape is non-rectangular, that would devalue all room checks
   > relying on size for room boundaries.
6. Write ShapeCollection::place_on(collection, offset). Offsets collection and
   appends its contents to the target collection.
7. Write ShapeCollection::draw_on(shape, offset).

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

> Databases work rather well now, though there's still the issue of having
> to start all entries with "name=" if I want to use weighted entries.
> Actually, that's what's keeping me from adding weights to the name
> generation.

Recently completed
==================

1. Implement databases to allow for subdirectories.
2. A* or similar pathfinding mechanism.
3. Find a good algorithm for compartmentalising the house into "domestic" and
   "utility" sections.
