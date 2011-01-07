
Table of Contents
=================

1. `Shape module`_

  A. `Shapes`_

    a. `Shape`_
    b. `Box`_
    c. `Column`_
    d. `ShapeColumn`_
    e. `ShapeRow`_

  B. `Collections`_

    a. `ShapeCollection`_
    b. `ShapeCoord`_

  C. `Shape Manipulation`_

    a. `adjoin`_
    b. `underneath`_
    c. `atop`_

  D. `Automatic shapes`_

    a. `AutoShape`_

  E. `Miscellaneous`_

    a. `ShapeError`_

2. `Coord module`_

  A. `Co-ordinates`_

    a. `Coord`_

  B. `Iterators`_

    a. `RectangleIterator`_

  C. `Sizes`_

    a. `Size`_

  D. `Automatic sizes and dimensions`_

    a. `AutoSize`_
    b. `AutoDimension`_

3. `Database module`_

  A. `Flat-text database`_

    a. `Database`_
    b. `get_databases`_
    c. `get_database`_
    d. `database_exists`_
    e. `num_databases`_

  B. `Weighted databases`_

    a. `WeightedString`_
    b. `WeightedDatabase`_

  C. `Database specifications`_

    a. `split_escaped_delim`_
    b. `parse_spec`_

4. `Documentation parser`_

  A. `Classes`_

    a. `Document`_
    b. `Module`_
    c. `Section`_

  B. `Methods`_

    a. `docparser`_

5. `Index`_

.. _Shape module:

Shape module
============

Shape, *a collection of clases and functions relating to Shapes*.

Shapes are a grid representation of ASCII graphics. Each point is denoted by an
x and y co-ordinate, where the co-ordinate 0, 0 is the top-left corner of any
shape. These shapes can be of any size, can be drawn onto each other, combined
into a single canvas, collected, split, sectioned, and iterated over.

See the `Shapes`_ section for ``Shape``, ``Box``, ``Column`` and related
classes.

See the `Collections`_ section for ``ShapeCollection`` and ``ShapeCoord``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shapes:

Shapes
------

Classes
#######

- `Shape`_.

 - `Box`_.
 - `Column`_.

- `ShapeColumn`_.
- `ShapeRow`_.

.. _Shape:

class *Shape*
^^^^^^^^^^^^^

Shapes consist of a canvas grid (with relative Coords). The shape can be
anything. Shapes can be drawn onto other shapes and have shapes drawn onto
them.

Direct glyph access is provided by Shape[x][y], Shape[Coord(x, y)].

Row and column access by ``row(number)`` and ``column(number)``. The ShapeRow
and ShapeColumns respectively returned by these are references to the Shape.
Modifications made to these will be reflected in the Shape.

Methods
#######

1. `Shape::__init__`_.
2. `Shape::column`_.
3. `Shape::draw_on`_.
4. `Shape::height`_.
5. `Shape::normalise`_.
6. `Shape::row`_.
7. `Shape::section`_.
8. `Shape::size`_.
9. `Shape::trim`_.
10. `Shape::width`_.
11. `Shape::__getitem__`_.
12. `Shape::__iter__`_.
13. `Shape::__setitem__`_.
14. `Shape::__str__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::__init__:

**Shape::__init__** (self, \*args, \*\*kwargs)

Create a new shape.

:``sh_list``: A list (or otherwise iterable) representation of a shape.
              For example, passing [list("...."), list("....")] will
              result in a 4x2 shape. If passed a Shape, will copy it and
              create a new shape. *Default None*.
:``width``: The width of the shape. If not 0, and ``sh_list`` has been
            provided, and the width is greater than the shape instatiated
            from ``sh_list``, the shape will be normalised to this width
            and ``fill``. If ``sh_list`` is not provided, the shape
            will be padded with ``fill``. *Default 0*.
:``height``: Likewise with ``width``. *Default 0*.
:``fill``: For padding purposes or blank, sized shapes, this character
           will be used to fill the canvas. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::column:

**Shape::column** (self, column)

Returns a ShapeColumn containing all the glyphs in ``column``. See the
ShapeColumn (closure) class definition for more information.

:``column``: The column to return. Required.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::draw_on:

**Shape::draw_on** (self, shape, offset=<Coord 0,0>, check_conflict=True, conflict_error=False)

Attempt to draw Shape instance ``shape`` on top of self, starting at
offset ``offset``. Conflict checking is enable by default (ie, it will
only draw glyphs from ``shape`` onto self if the relevant co-ordinate is
None), but by default it will simply ignore errors.

:``shape``: The shape which will be drawn upon this one. It is
            presumed that this shape can be contained by self.
            *Required*.
:``offset``: The co-ordinates to begin drawing at (ie, starting with
             the top left corner of ``shape`` (0, 0), it will begin
             drawing from here). *Default 0, 0*.
:``check_conflict``: Check for conflict before drawing. If true, it
                     will only copy a glyph from ``shape`` onto self if
                     self contains None at that location. *Default
                     True*.
:``conflict_error``: If true, will raise a ShapeError upon conflicts.
                     Catching this error allows the detection of
                     accidental overwriting. *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::height:

**Shape::height** (self)

Returns the smallest height that can contain the largest column of
the shape. *Note: columns are uniform in size across the shape; as with
rows, None padding is counted.*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::normalise:

**Shape::normalise** (self, width=None, height=None, fill=None)

Extend either the width, the height, or both, of a Shape to the relevant
value, using the provided fill value.

:``width``: The width to which the Shape should be extended. This
            integer value should be greater than the current width
            of the Shape, or None to perform no width normalisation.
            *Default None*.
:``height``: The height to which the Shape should be extended. As per
             ``width`` above. *Default None*.
:``fill``: The fill character which should be used when extending
           rows and columns. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::row:

**Shape::row** (self, row)

Returns a ShapeRow containing all the glyphs in ``row``. See the
ShapeRow (closure) class definition for more information.

:``row``: The row to return. Required.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::section:

**Shape::section** (self, section_start, section_stop=None)

Return a new Shape containing within it the content of the current shape
from ``section_start`` to ``section_stop``.

:``section_start``: The top left co-ordinates of the rectangle. If
                    ``section_stop`` has not been provided, it will be
                    assumed that the section should instead consist of
                    Coord(0, 0) to ``section_stop``.
:``section_stop``: The bottom right co-ordinates of the rectangle. See
                   note regarding ``section_start``. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::size:

**Shape::size** (self)

Returns the smallest box that can contain the shape. *Note: this counts
padding characters (None) as normal glyphs. Thus, it is only possible
to have varying lengths of rows, with the 'gap' being represented on
the right side of the object.*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::trim:

**Shape::trim** (self, width=None, height=None, trim_left=False, trim_top=False)

The opposite of normalise in that it reduces the size of a Shape to the
relevant width or height provided. For reducing width, it can remove
columns from the right (default) or the left of the shape. For reducing
height, it can remove rows from the bottom (default) or the top of the
shape.

:``width``: As per normalise, the number of columns to reduce the
            shape to. Note: this is not the number of columns to
            remove. *Default None*.
:``height``: As per width, only regarding rows.
:``trim_left``: Instead remove columns from the left of the shape.
                *Default False*.
:``trim_top``: Instead remove rows from the top of the shape. *Default*
               *False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::width:

**Shape::width** (self)

Returns the smallest width that can contain the largest row of the
shape. *Note: rows padded with None are not equivalent in length
to rows without padding.*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::__getitem__:

**Shape::__getitem__** (self, item)

Return either a glyph (if ``item`` is a Coord), or a column (if ``item``
is an integer). Does **not** support slicing!

:``item``: Either a Coord, in which case we return the actual item, or
           an "x" axis integer. The latter will return a ShapeColumn
           object that references the column.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::__iter__:

**Shape::__iter__** (self)

Provide an iterator that returns (Coord(x, y), self[x][y]) for each
glyph within the Shape.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::__setitem__:

**Shape::__setitem__** (self, item, value)

Alter the glyph at ``item`` by replacing with ``value``. Does **not**
support slicing.

:``item``: A co-ordinate, in which case we perform direct assignation
           of ``value`` to ``item``. The syntax of Shape[x][y] will not
           actually be parsed by this function. Instead, it is parsed
           as Shape.column(x)[y].
:``value``: Either None, a single-character string, or a list, instance
            of Shape or its subclass, Column. If passed a 1*x Shape it
            will attempt to draw the Shape on top of itself (without
            checking for conflict).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape::__str__:

**Shape::__str__** (self)

Translate a Shape into a string. None values are replaced with " ", and
new lines ("\n") are inserted at the end of each row.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Box:

class *Box*
^^^^^^^^^^^

A rectangular Shape that provides borders and perimeter access.

Methods
#######

1. `Box::__init__`_.
2. `Box::perimeter`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Box::__init__:

**Box::__init__** (self, width, height, border=1, fill=None, border_fill=None)

Create a box.

:``width``: How many characters wide the box should be.
:``height``: How many characters tall the box should be.
:``border``: The size of border to place. *Default 1*.
:``fill``: The fill character of the box. *Default None*.
:``border_fill``: The character to use when generating the border which
                  is drawn on top of the fill character (regardless of
                  conflicts).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Box::perimeter:

**Box::perimeter** (self)

Returns an iterator of Coords corresponding to the perimeter of the box,
specifically the border define when initialising the box. If
``self.border`` == 0 then will return nothing.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Column:

class *Column*
^^^^^^^^^^^^^^

A single-character column of characters.

Methods
#######

1. `Column::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Column::__init__:

**Column::__init__** (self, shape=None, height=None, fill=None)

Create a column.

:``shape``: List of characters (or Shape or ShapeColumn) to fill our
            column with.
:``height``: Height to pad the column to. *Default None*.
:``fill``: Padding character to use when padding the column. *Default
           None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn:

class *ShapeColumn*
^^^^^^^^^^^^^^^^^^^

ShapeColumn is merely a reference to a specific column of glyphs in a parent
Shape class. It's implemented thus to allow swapping of the x and y
co-ordinates when accessing a Shape as though it were a multi-dimensional
array.

Modifying via index (ShapeColumn[1]=None, for instance) will in fact
modify the Shape.

Methods
#######

1. `ShapeColumn::col`_.
2. `ShapeColumn::copy`_.
3. `ShapeColumn::parent`_.
4. `ShapeColumn::__getitem__`_.
5. `ShapeColumn::__iter__`_.
6. `ShapeColumn::__repr__`_.
7. `ShapeColumn::__setitem__`_.
8. `ShapeColumn::__str__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::col:

**ShapeColumn::col** (self)

Returns the column number that this column is a representation of.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::copy:

**ShapeColumn::copy** (self)

Returns the actual column object as a list. This column object is a
copy, and any edits made to it are not reflected in the Shape.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::parent:

**ShapeColumn::parent** (self)

Returns the Shape to which this column belongs.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::__getitem__:

**ShapeColumn::__getitem__** (self, row)

Returns the glpyh located at ``row``.

:``row``: The row being requested for.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::__iter__:

**ShapeColumn::__iter__** (self)

Provides iteration over the content of the column in the format of:
tuple(Coord, glyph), where Coord equates to the glyph location in the
Shape (rather than in this column), and the glyph is the relevant glyph.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::__repr__:

**ShapeColumn::__repr__** (self)

Returns a representation of the column as an object.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::__setitem__:

**ShapeColumn::__setitem__** (self, row, value)

Performs in-place assignation via ``self.parent()[Coord(self.column, row)]``
``= value`` (roughly). In fact, as the class is a closure, it does none of
these.

Provides index-based row access to the column, ie, column[1]="x".

:``row``: The row that you wish to assign a value to.
:``value``: The glyph you want to place. Either len(``value``) == 1
            or ``value`` is None must be true for the assignation to
            be successful.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeColumn::__str__:

**ShapeColumn::__str__** (self)

Returns a string representation of the column, where each glyph is
followed by a new line.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow:

class *ShapeRow*
^^^^^^^^^^^^^^^^

ShapeRow is merely a reference to a specific row of glyphs in a parent Shape
class. It reflects the implementation of the ShapeColumn which is thus
implemented to allow swapping x and y co-ordinates when accessing a shape as
though it were a multi-dimensional list.

Modifying via index (ShapeRow[1]=None, for instance) will in fact modify the
Shape.

Methods
#######

1. `ShapeRow::copy`_.
2. `ShapeRow::parent`_.
3. `ShapeRow::row`_.
4. `ShapeRow::__getitem__`_.
5. `ShapeRow::__iter__`_.
6. `ShapeRow::__repr__`_.
7. `ShapeRow::__setitem__`_.
8. `ShapeRow::__str__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::copy:

**ShapeRow::copy** (self)

Returns the actual row object as a list. This row object is a
copy, and any edits made to it are not reflected in the Shape.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::parent:

**ShapeRow::parent** (self)

Returns the Shape to which this row belongs.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::row:

**ShapeRow::row** (self)

Returns the row number that this row is a representation of.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::__getitem__:

**ShapeRow::__getitem__** (self, column)

Returns the glpyh located at ``column``.

:``column``: The column being requested for.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::__iter__:

**ShapeRow::__iter__** (self)

Provides iteration over the content of the row in the format of:
tuple(Coord, glyph), where Coord equates to the glyph location in the
Shape (rather than in this row), and the glyph is the relevant glyph.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::__repr__:

**ShapeRow::__repr__** (self)

Returns a representation of the row as an object.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::__setitem__:

**ShapeRow::__setitem__** (self, column, value)

Performs in-place assignation via self.parent()[Coord(self.row, column)]
= value (roughly). In fact, as the class is a closure, it does none of
these.

Provides index-based column access to the row, ie, row[1]="x".

:``column``: The column that you wish to assign a value to.
:``value``: The glyph you want to place. Either len(``value``) == 1
            or ``value`` is None must be true for the assignation to
            be successful.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeRow::__str__:

**ShapeRow::__str__** (self)

Returns a string representation of the row.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Collections:

Collections
-----------

Classes
#######

- `ShapeCollection`_.
- `ShapeCoord`_.

.. _ShapeCollection:

class *ShapeCollection*
^^^^^^^^^^^^^^^^^^^^^^^

A sortable collection of Shapes and co-ordinates. Can be initiliased from a list
of ShapeCoords or Shapes. For the latter, these will be wrapped in a ShapeCoord
using Coord(0, 0) as their co-ordinate.

You can also ``append`` items, ``pop`` items, assign using ShapeCollection[index]
notation, and fetch via ShapeCollcetion[index] notation.

Methods
#######

1. `ShapeCollection::__init__`_.
2. `ShapeCollection::append`_.
3. `ShapeCollection::combine`_.
4. `ShapeCollection::copy`_.
5. `ShapeCollection::height`_.
6. `ShapeCollection::pop`_.
7. `ShapeCollection::size`_.
8. `ShapeCollection::sort`_.
9. `ShapeCollection::width`_.
10. `ShapeCollection::__getitem__`_.
11. `ShapeCollection::__iter__`_.
12. `ShapeCollection::__len__`_.
13. `ShapeCollection::__setitem__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__init__:

**ShapeCollection::__init__** (self, shapes=None)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::append:

**ShapeCollection::append** (self, item, coord=None)

As with the initialisation function, all Shapes passed in are here
converted into ShapeCoords, using Coord(0, 0) as their offset. All other
instances are not allowed.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::combine:

**ShapeCollection::combine** (self)

Converts a collection into a single Shape by taking drawing all ShapeCoords
onto an automatically shaped canvas.

Doesn't currently provide error checking. Should.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::copy:

**ShapeCollection::copy** (self)

Returns a copy of this collection.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::height:

**ShapeCollection::height** (self)

Returns the height required to contain each member.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::pop:

**ShapeCollection::pop** (self, index=-1)

Pop index ``index`` item from the collection of ShapeCoords.

:``index``: The index in question. *Default -1*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::size:

**ShapeCollection::size** (self)

Returns the size required to contain each member.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::sort:

**ShapeCollection::sort** (self)

In-place sorting by size!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::width:

**ShapeCollection::width** (self)

Returns the width required to contain each member.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__getitem__:

**ShapeCollection::__getitem__** (self, item)

Fetch item index ``item`` from the collection of ShapeCoords.

:``item``: The item to be fetched.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__iter__:

**ShapeCollection::__iter__** (self)

Creates an iterator for the ShapeCoords contained within.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__len__:

**ShapeCollection::__len__** (self)

Returns the number of ShapeCoords contained within.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__setitem__:

**ShapeCollection::__setitem__** (self, item, value)

Insert ``value`` at ``item``, replacing whatever ShapeCoord is existent
there.

:``item``: The index the value is to be inserted at.
:``value``: The value to be inserted. This is automatically cased
            from a Shape into a ShapeCoord(Shape, Coord(0, 0)).
            Otherwise it is assumed to be a ShapeCoord. All other
            types will cause an error.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCoord:

class *ShapeCoord*
^^^^^^^^^^^^^^^^^^

A named tuple pair providing ``shape`` and ``coord`` members. This is primarily
used by the ShapeCollection class.

Methods
#######

1. `ShapeCoord::height`_.
2. `ShapeCoord::size`_.
3. `ShapeCoord::width`_.
4. `ShapeCoord::__getattribute__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCoord::height:

**ShapeCoord::height** (self)

Wrapper over self.shape.height.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCoord::size:

**ShapeCoord::size** (self)

Wrapper over self.shape.size.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCoord::width:

**ShapeCoord::width** (self)

Wraper over self.shape.width.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCoord::__getattribute__:

**ShapeCoord::__getattribute__** (self, attr)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Shape Manipulation:

Shape Manipulation
------------------

Methods
#######

.. _adjoin:

function *adjoin* (shape1, shape2, overlap=0, fill=None, join_left=False, skip_conflicts=False, collection=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take two shapes and combine them into one. This method places shapes
side-by-side with ``shape1`` on the left and ``shape2`` on the right. If
``overlap`` is greater than zero, ``shape2`` will overlap ``shape1`` on the
left by ``overlap``. Finally, the resultant shape will be padded using
``fill``.

:``shape1``: The first shape. *Required*.
:``shape2``: The second shape. *Required*.
:``overlap``: How much to overlap ``shape1`` with ``shape2``. *Default*
              *0*.
:``fill``: The character to pad out the rest of the canvas if
           ``shape1.height() < shape2.height()`` or vice versa.
:``join_left``: If true, will instead join ``shape2`` to the left of
                ``shape1``. This is achieved by swapping the parameters.
                *Default False*.
:``skip_conflicts``: If true and ``overlap`` > 0, will not draw the parts of
                     ``shape2`` where they overlap with the parts of ``shape1``.
:``collection``: If true, returns a ShapeCollection instead of a canvas.
                 *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _underneath:

function *underneath* (shape1, shape2, left_offset=0, overlap=0, fill=None, join_top=False, skip_conflicts=False, offset_first=False, offset_second=True, collection=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take two shapes and combine them into one by drawing ``shape1`` and then
drawing ``shape2`` directly beneath it.

:``shape1``: The first shape to be drawn. *Required*.
:``shape2``: The second shape to be drawn; this will be drawn
             underneath ``shape1``. *Required*.
:``left_offset``: How many columns to offset the shapes by. *Default 0*.
:``overlap``: How many rows ``shape2`` should overlap ``shape1``.
              *Default 0*.
:``fill``: Character to be used in filling out the canvas.
           *Default None*.
:``join_top``: Draw ``shape2`` on top of ``shape1`` instead. *Default*
               *False*.
:``skip_conflicts``: Where ``shape2`` conflicts with ``shape1``, keep
                     ``shape1``'s glyphs. *Default False*
:``offset_first``: Offset ``shape1`` by ``left_offset``. *Default False*.
:``offset_second``: Offset ``shape2`` by ``left_offset``. *Default True*.
:``collection``: If true, returns a ShapeCollection instead of a canvas.
                 *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _atop:

function *atop* (shape1, shape2, left_offset=0, overlap=0, fill=None, join_bottom=False, skip_conflicts=False, offset_first=False, offset_second=True, collection=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take two shapes and combine them into one by drawing ``shape1`` and then
drawing ``shape2`` directly above it. This is an alias for ``underneath``
with the ``join_top`` flag set to True.

:``shape1``: The first shape to be drawn. *Required*.
:``shape2``: The second shape to be drawn; this will be drawn
             above ``shape1``. *Required*.
:``left_offset``: How many columns to offset the shapes by. *Default 0*.
:``overlap``: How many rows ``shape2`` should overlap ``shape1``.
              *Default 0*.
:``fill``: Character to be used in filling out the canvas.
           *Default None*.
:``join_bottom``: Draw ``shape2`` beneath of ``shape1`` instead. *Default*
                  *False*.
:``skip_conflicts``: Where ``shape2`` conflicts with ``shape1``, keep
                     ``shape1``'s glyphs. *Default False*
:``offset_first``: Offset ``shape1`` by ``left_offset``. *Default False*.
:``offset_second``: Offset ``shape2`` by ``left_offset``. *Default True*.
:``collection``: If true, returns a ShapeCollection instead of a canvas.
                 *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Automatic shapes:

Automatic shapes
----------------

Classes
#######

- `AutoShape`_.

.. _AutoShape:

class *AutoShape*
^^^^^^^^^^^^^^^^^

An unsized Shape that expands to suit needs.

Methods
#######

1. `AutoShape::__init__`_.
2. `AutoShape::actual_height`_.
3. `AutoShape::actual_size`_.
4. `AutoShape::actual_width`_.
5. `AutoShape::height`_.
6. `AutoShape::normalise`_.
7. `AutoShape::size`_.
8. `AutoShape::width`_.
9. `AutoShape::_actual_wrapper`_.
10. `AutoShape::__getitem__`_.
11. `AutoShape::__setitem__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::__init__:

**AutoShape::__init__** (self, fill=None)

Initiate the automatic shape.

:``fill``: What character should be used when normalising the shape.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_height:

**AutoShape::actual_height** (self)

To compensate for automatic sizing, actual heights of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_size:

**AutoShape::actual_size** (self)

To compensate for automatic sizing, actual sizes of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_width:

**AutoShape::actual_width** (self)

To compensate for automatic sizing, actual widths of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::height:

**AutoShape::height** (self)

To compensate for the automatic sizing of the shape, height returns an
"infinite" height. To get the actual height of the shape, use
``AutoShape::actual_width``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::normalise:

**AutoShape::normalise** (self, \*args, \*\*kwargs)

Extend either the width, the height, or both, of a Shape to the relevant
value, using the provided fill value.

:``width``: The width to which the Shape should be extended. This
            integer value should be greater than the current width
            of the Shape, or None to perform no width normalisation.
            *Default None*.
:``height``: The height to which the Shape should be extended. As per
             ``width`` above. *Default None*.
:``fill``: The fill character which should be used when extending
           rows and columns. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::size:

**AutoShape::size** (self)

To compensate for the automatic sizing of the shape, size returns an
"infinite" size. To get the actual size of the shape, use
``AutoShape::actual_size.``

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::width:

**AutoShape::width** (self)

To compensate for the automatic sizing of the shape, width returns an
"inifinite" width. To get the actual width of the shape, use
``AutoShape::actual_width``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::_actual_wrapper:

**AutoShape::_actual_wrapper** (function)

Performs hot-swapping of actual_width, actual_height and actual_size
into the relevant width, height and size functions before executing
the function. Once performed, hot-swaps the functions back again.

:``function``: The function to be wrapped.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::__getitem__:

**AutoShape::__getitem__** (self, item)

Attempt to access ``item``. If ``item`` is outside of the bounds of the
current shape, it is sized accordingly.

:``item``: The item to be accessed.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::__setitem__:

**AutoShape::__setitem__** (self, item, value)

Attempt to set ``item`` to ``value``. If ``item`` if outside of the
bounds of the current shape, it is sized accordingly.

:``item``: The item to be set.
:``value``: The value to be set.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Miscellaneous:

Miscellaneous
-------------

Classes
#######

- `ShapeError`_.

.. _ShapeError:

class *ShapeError*
^^^^^^^^^^^^^^^^^^

A generic Shape-related error.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Coord module:

Coord module
============

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Co-ordinates:

Co-ordinates
------------

Classes
#######

- `Coord`_.

.. _Coord:

class *Coord*
^^^^^^^^^^^^^

Simple representation of a co-ordinate. 0,0 is assumed to be the top-left
base co-ordinate. A co-ordinate defined as -1,-1 is assumed to be invalid.
However, negative co-ordinates may be useful for co-ordinate arithmetic.

Methods
#######

1. `Coord::__init__`_.
2. `Coord::as_tuple`_.
3. `Coord::valid`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Coord::__init__:

**Coord::__init__** (self, x=-1, y=-1)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Coord::as_tuple:

**Coord::as_tuple** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Coord::valid:

**Coord::valid** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Iterators:

Iterators
---------

Classes
#######

- `RectangleIterator`_.

.. _RectangleIterator:

class *RectangleIterator*
^^^^^^^^^^^^^^^^^^^^^^^^^

Methods
#######

1. `RectangleIterator::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _RectangleIterator::__init__:

**RectangleIterator::__init__** (self, start_point, stop_point=None)

Iterator over a rectangle of points starting at ``start_point``, finishing
at ``stop_point``.

:``start_point``: The starting location of rectangle; if ``stop_point``
                  is undefined, ``start_point`` will become ``Coord(0,0)``
                  and the original start point will be used as the stop
                  point. *Required*.
:``stop_point``: The finishing location of the rectangle. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Sizes:

Sizes
-----

Classes
#######

- `Size`_.

.. _Size:

class *Size*
^^^^^^^^^^^^

A specific representation of size using width and height.

Methods
#######

1. `Size::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Size::__init__:

**Size::__init__** (self, width=-1, height=-1)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Automatic sizes and dimensions:

Automatic sizes and dimensions
------------------------------

Classes
#######

- `AutoDimension`_.
- `AutoSize`_.

.. _AutoSize:

class *AutoSize*
^^^^^^^^^^^^^^^^

An automatic size. For comparative purposes, it is always larger than
something else--never equal and never smaller.

Methods
#######

1. `AutoSize::__init__`_.
2. `AutoSize::valid`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoSize::__init__:

**AutoSize::__init__** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoSize::valid:

**AutoSize::valid** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoDimension:

class *AutoDimension*
^^^^^^^^^^^^^^^^^^^^^

An automatically sized integer. As a string, it is represented by infinity.
It is always larger than other integers, never less than nor equal to.

Methods
#######


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database module:

Database module
===============

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Flat-text database:

Flat-text database
------------------

Classes
#######

- `Database`_.

Methods
#######

.. _Database:

class *Database*
^^^^^^^^^^^^^^^^

An extremely simplistic type that is nothing more than a wrapper on top of
the default list type.

Methods
#######

1. `Database::__init__`_.
2. `Database::copy`_.
3. `Database::random`_.
4. `Database::random_pop`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database::__init__:

**Database::__init__** (self, name, data)

Initialises the database.

:``name``: The name of the Database. This is stored and used to describe
           the database.
:``data``: The actual data of the Database. This should be a list of
           items in any format.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database::copy:

**Database::copy** (self)

Returns a copy of the database that allows for modification.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database::random:

**Database::random** (self, checkfn=None)

Returns a random element from the Database.

:``checkfn``: A function to be applied to results. If this function
              returns ``true``, the result is allowed; if it returns
              ``false``, another item is picked. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database::random_pop:

**Database::random_pop** (self, checkfn=None)

Removes a random element from the Database and then returns it. This is
an in-place activity.

:``checkfn``: A function to be applied to results. If this function
              returns ``true``, the result is allowed; if it returns
              ``false``, another item is picked. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_databases:

function *get_databases* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a list of all Database objects stored.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_database:

function *get_database* (name)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a specific Database object. If the Database doesn't exist, will
instead return ``None``.

:``name``: The name of the Database object being requested.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _database_exists:

function *database_exists* (name)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Checks for the existance of a specific database object.

:``name``: The name of the Database.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _num_databases:

function *num_databases* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns the total number of Databases available.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Weighted databases:

Weighted databases
------------------

Classes
#######

- `WeightedString`_.
- `WeightedDatabase`_.

.. _WeightedString:

class *WeightedString*
^^^^^^^^^^^^^^^^^^^^^^

A simple collation of a string and a weight.

The default weight of ``10`` means that the string has no higher or lesser
chance of being chosen from a WeightedDatabase than any other string.  A
weight of ``20`` means that it has double the chance, a weight of ``5``
meaning that has half the chance, etc.

Methods
#######

1. `WeightedString::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedString::__init__:

**WeightedString::__init__** (self, string, weight=10)

Create a new weighted string.

:``string``: The actual string contents.
:``weight``: The weight of the string. *Default 10*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedDatabase:

class *WeightedDatabase*
^^^^^^^^^^^^^^^^^^^^^^^^

A slightly more complicated collection of data stored by weight. The
"default" weight of the databse is ``10``. Random choices pick things by
weight as well as randomness, etc.

Methods
#######

1. `WeightedDatabase::random`_.
2. `WeightedDatabase::random_pick`_.
3. `WeightedDatabase::random_pop`_.
4. `WeightedDatabase::total_weight`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedDatabase::random:

**WeightedDatabase::random** (self, checkfn=None)

Returns a random element from the Database, picked by weight.

:``checkfn``: A function to be applied to the items in the database: if
              it returns ``false``, the item is not considered. *Default
              None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedDatabase::random_pick:

**WeightedDatabase::random_pick** (self, checkfn=None)

Randomly pick an item from the database based on its weight in
comparison to the total weight of the database. Returns a tuple of
(``index``, ``item``).

:``checkfn``: A function to be applied to the items in the database: if
              it returns ``false``, the item is not considered. *Default
              None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedDatabase::random_pop:

**WeightedDatabase::random_pop** (self, checkfn=None)

Removes a random element from the Database and then returns it. This is
an in-place activity.

:``checkfn``: A function to be applied to the items in the database: if
              it returns ``false``, the item is not considered. *Default
              None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _WeightedDatabase::total_weight:

**WeightedDatabase::total_weight** (self, checkfn=None)

Return the total weight of the database.

:``checkfn``: A function to be applied to each item. If the function
              returns ``false``, the weight of the item is ignored (and the
              item is discarded). *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Database specifications:

Database specifications
-----------------------

Methods
#######

.. _split_escaped_delim:

function *split_escaped_delim* (delimiter, string, count=0)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns the result of splitting ``string`` with ``delimiter``. It is an
extension of ``string.split(delimiter, count)`` in that it ignores instances
of the delimiter being escaped or contained within a string.

:``delimiter``: The delimiter to split the string with. *Required*.
:``string``: The string to be split. *Required*.
:``count``: How many strings to limit the match to. *Default 0*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _parse_spec:

function *parse_spec* (spec_file)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parses a specification into either a list or a namedtuple constructor.

**Example specifications**::

    $0

*Would return a single-element list creator that could be applied to all
incoming data.*::

    %delim ,
    $0
    $1
    $2

*Would return a three-element list creator using "," as the delimiter.*::

    $name
    $weight 10

*Would return a two-element namedtuple called "(filename)_spec" with a name
and weight property. The weight would default to 10 if not supplied.*::

    %id room_spec
    $name
    $weight

*Would return a two-element namedtuple called "room_spec" with a name and
weight property.*

**Example specification usage**::

    (using the "room_spec" above)
    %
    name=dining room
    %
    name=kitchen
    weight=20

In this instance, the order doesn't matter, as they are passed by
parameter::

    (using the first unnamed list example)
    %
    dining room
    %
    kitchen
    %

As there is just a single set of data, the block is parsed and stripped of
whitespace and then stored in a single element::

    (using the second unnamed list example)
    %
    dining room,10,domestic
    %
    kitchen, 50, utility
    %

Here, the provided delimiter of a commas used to convert the incoming block
into a three-element list.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Documentation parser:

Documentation parser
====================

docparser, a quick parser for documentation configuration.

This converts a flat representation of what methods and classes of what modules
should be documented, and in which sections, from text into an iterable
document. The file format for \*.conf files allows combinations of the following
signifiers:

:`$ignore`_: ``qualified name``
:`$module`_: ``module identifier``, ``module description``
:`$suppress`_: ``suppression target`` [1]_
:`$section`_: ``section description`` [2]_
:`$classes`_: ``class1``, ``class2``, ... [3]_
:`$methods`_:  ``method1``, ``method2``, ... [3]_
:``#``: ``comment text`` [4]_

.. [1] Suppression targets are defined per-module, thus must be included in a
       block of module definitions.
.. [2] Section sigifiers are associated with the most recent module signifier.
       If there is no previous module, they are discarded.
.. [3] Lists of classes and methods are associated with sections, and if there is no
       previous section signifier, they are discarded.
.. [4] Comments are simply ignored by the parser. Any line beginning with the
       ``#`` symbol will be skipped during parsing.

.. _$ignore:

``$ignore``
-----------

Arguments:

:``qualified name``: A string in the format of *function name* or *class
                     name::function name*.

``$ignore`` has two specific behaviours. If passed a non-qualified function
name, this function will be ignored when iterating over class members *if and
only if* the method is undocumented.

If passed a qualified class function name, this function will always be ignored.

*Examples*:

``$ignore __repr__``: All undocumented ``__repr__`` methods will be suppressed
from display.

``$ignore Document::__init__``: The ``__init__`` method of the ``Document``
class will be suppressed from display, regardless of whether or not it has been
documented.

All ``$ignore`` signifiers must be followed by a single string. To denote
multiple functions or methods to be ignored, use multiple ``$ignore``
signifiers, each with its own line.

.. _$module:

``$module``
-----------

Arguments:

:``module identifier``: Must be a valid Python module identifier, and located in
                        the path. Must be unique.
:``module description``: A short string description of the module. Used for
                         generating module headers.

Definine a ``$module`` begins a new module block. If a module block has already
been begun, that module is closed and the result appended to the document's
module list. Defining a module allows for the definition of sections.

.. _$suppress:

``$suppress``
-------------

Arguments:

:``suppression target``: One of: "toc".

Currently, this only supports the suppression of, per-module, generating a table
of contents.

.. _$section:

``$section``
------------

Arguments:

:``section description``: A string used for section headlines. Must be unique.

Sections denote the beginning of a new block. If a previous section has been
defined, that section will be closed and appended to the current module. To
specify classes and modules that are to be documented, they must be associated
with a specific section.

.. _$classes:

``$classes``
------------

Arguments:

:[``class1``, ``class2``, ``...``]: A list of comma separated classes to be
                                    recursively documented. [3]_

.. _$methods:

``$methods``
------------

Arguments:

:[``method1``, ``method2``, ``...``]: A list of comma separated methods to be
                                      documented. [3]_

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Classes:

Classes
-------

Classes
#######


.. _Document:

class *Document*
^^^^^^^^^^^^^^^^

Defines an iterable list of modules and ignore targets.

Members
#######

:``modules``: A list of ``Module`` relevant to this document.
:``ignore``: A list of ignore targets relevant to this document.

Methods
#######

1. `Document::__iter__`_.
2. `Document::__str__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Document::__iter__:

**Document::__iter__** (self)

Yields a tuple of three values: ``module``, ``section`` and ``object``.
Some or all of these may be ``None``. Specifically, iteration begins by
yielding (``Module``, ``None``, ``None``)``; it then steps into the
module and yields (``Module``, ``Section``, ``None``); it then steps
into the section and yields (``Module``, ``Section``, ``Obj``) for each
class and method the section defines, if any; finally, once it has
reached the bottom of any tree, it steps back a level (from objects to
sections, for instance) and tries the next tree; if there is no next
tree, it steps back again, until finally all modules, their sections,
and subsequent class or method lists have been exhausted.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Document::__str__:

**Document::__str__** (self)

Provides a tree-like representation of the document.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Module:

class *Module*
^^^^^^^^^^^^^^

Stores information about a Python module to be documented.

Members
#######

:``sections``: A list of ``Sections`` relevant to this module.

Methods
#######

1. `Module::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Module::__init__:

**Module::__init__** (self, name=None)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Section:

class *Section*
^^^^^^^^^^^^^^^

Stores information about a section of a Python module to be documented.

Members
#######

:``classes``: A list of strings of classes defined by the module.
:``methods``: A list of strings of methods defined by the module.

Methods
#######

1. `Section::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Section::__init__:

**Section::__init__** (self, name=None)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Methods:

Methods
-------

Methods
#######

.. _docparser:

function *docparser* (filename, verbose=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterators over the provided filename, parses it, and returns a ``Document``.

:``filename``: The filename to iterate over. Can either be a: ``file``
               instance; a list of strings; a single, new line separated
               string; or a string representing a file name.
:``verbose``: If True, will provide parse-time messages about encountered
              signifiers, etc. *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+-------------------------------------+-------------------------------------+
|`adjoin`_                            |`atop`_                              |
+-------------------------------------+-------------------------------------+
|`AutoDimension`_                     |`AutoShape`_                         |
+-------------------------------------+-------------------------------------+
|`AutoShape::__init__`_               |`AutoShape::actual_height`_          |
+-------------------------------------+-------------------------------------+
|`AutoShape::actual_size`_            |`AutoShape::actual_width`_           |
+-------------------------------------+-------------------------------------+
|`AutoShape::height`_                 |`AutoShape::normalise`_              |
+-------------------------------------+-------------------------------------+
|`AutoShape::size`_                   |`AutoShape::width`_                  |
+-------------------------------------+-------------------------------------+
|`AutoShape::_actual_wrapper`_        |`AutoShape::__getitem__`_            |
+-------------------------------------+-------------------------------------+
|`AutoShape::__setitem__`_            |`AutoSize`_                          |
+-------------------------------------+-------------------------------------+
|`AutoSize::__init__`_                |`AutoSize::valid`_                   |
+-------------------------------------+-------------------------------------+
|`Box`_                               |`Box::__init__`_                     |
+-------------------------------------+-------------------------------------+
|`Box::perimeter`_                    |`Column`_                            |
+-------------------------------------+-------------------------------------+
|`Column::__init__`_                  |`Coord`_                             |
+-------------------------------------+-------------------------------------+
|`Coord::__init__`_                   |`Coord::as_tuple`_                   |
+-------------------------------------+-------------------------------------+
|`Coord::valid`_                      |`Database`_                          |
+-------------------------------------+-------------------------------------+
|`Database::__init__`_                |`Database::copy`_                    |
+-------------------------------------+-------------------------------------+
|`Database::random`_                  |`Database::random_pop`_              |
+-------------------------------------+-------------------------------------+
|`database_exists`_                   |`docparser`_                         |
+-------------------------------------+-------------------------------------+
|`Document`_                          |`Document::__iter__`_                |
+-------------------------------------+-------------------------------------+
|`Document::__str__`_                 |`get_database`_                      |
+-------------------------------------+-------------------------------------+
|`get_databases`_                     |`Module`_                            |
+-------------------------------------+-------------------------------------+
|`Module::__init__`_                  |`num_databases`_                     |
+-------------------------------------+-------------------------------------+
|`parse_spec`_                        |`RectangleIterator`_                 |
+-------------------------------------+-------------------------------------+
|`RectangleIterator::__init__`_       |`Section`_                           |
+-------------------------------------+-------------------------------------+
|`Section::__init__`_                 |`Shape`_                             |
+-------------------------------------+-------------------------------------+
|`Shape::__init__`_                   |`Shape::column`_                     |
+-------------------------------------+-------------------------------------+
|`Shape::draw_on`_                    |`Shape::height`_                     |
+-------------------------------------+-------------------------------------+
|`Shape::normalise`_                  |`Shape::row`_                        |
+-------------------------------------+-------------------------------------+
|`Shape::section`_                    |`Shape::size`_                       |
+-------------------------------------+-------------------------------------+
|`Shape::trim`_                       |`Shape::width`_                      |
+-------------------------------------+-------------------------------------+
|`Shape::__getitem__`_                |`Shape::__iter__`_                   |
+-------------------------------------+-------------------------------------+
|`Shape::__setitem__`_                |`Shape::__str__`_                    |
+-------------------------------------+-------------------------------------+
|`ShapeCollection`_                   |`ShapeCollection::__init__`_         |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::append`_           |`ShapeCollection::combine`_          |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::copy`_             |`ShapeCollection::height`_           |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::pop`_              |`ShapeCollection::size`_             |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::sort`_             |`ShapeCollection::width`_            |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::__getitem__`_      |`ShapeCollection::__iter__`_         |
+-------------------------------------+-------------------------------------+
|`ShapeCollection::__len__`_          |`ShapeCollection::__setitem__`_      |
+-------------------------------------+-------------------------------------+
|`ShapeColumn`_                       |`ShapeColumn::col`_                  |
+-------------------------------------+-------------------------------------+
|`ShapeColumn::copy`_                 |`ShapeColumn::parent`_               |
+-------------------------------------+-------------------------------------+
|`ShapeColumn::__getitem__`_          |`ShapeColumn::__iter__`_             |
+-------------------------------------+-------------------------------------+
|`ShapeColumn::__repr__`_             |`ShapeColumn::__setitem__`_          |
+-------------------------------------+-------------------------------------+
|`ShapeColumn::__str__`_              |`ShapeCoord`_                        |
+-------------------------------------+-------------------------------------+
|`ShapeCoord::height`_                |`ShapeCoord::size`_                  |
+-------------------------------------+-------------------------------------+
|`ShapeCoord::width`_                 |`ShapeCoord::__getattribute__`_      |
+-------------------------------------+-------------------------------------+
|`ShapeError`_                        |`ShapeRow`_                          |
+-------------------------------------+-------------------------------------+
|`ShapeRow::copy`_                    |`ShapeRow::parent`_                  |
+-------------------------------------+-------------------------------------+
|`ShapeRow::row`_                     |`ShapeRow::__getitem__`_             |
+-------------------------------------+-------------------------------------+
|`ShapeRow::__iter__`_                |`ShapeRow::__repr__`_                |
+-------------------------------------+-------------------------------------+
|`ShapeRow::__setitem__`_             |`ShapeRow::__str__`_                 |
+-------------------------------------+-------------------------------------+
|`Size`_                              |`Size::__init__`_                    |
+-------------------------------------+-------------------------------------+
|`split_escaped_delim`_               |`underneath`_                        |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase`_                  |`WeightedDatabase::random`_          |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase::random_pick`_     |`WeightedDatabase::random_pop`_      |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase::total_weight`_    |`WeightedString`_                    |
+-------------------------------------+-------------------------------------+