
Table of Contents
=================

1. `Shape module`_

  A. `Shapes`_

    a. `Shape`_
    b. `Box`_
    c. `Column`_
    d. `ShapeColumn`_
    e. `ShapeRow`_

  B. `Shape Manipulation`_

    a. `adjoin`_
    b. `underneath`_
    c. `atop`_

  C. `Automatic shapes`_

    a. `AutoShape`_

  D. `Miscellaneous`_

    a. `ShapeError`_

2. `Index`_

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
11. `Shape::wipe`_.
12. `Shape::__getitem__`_.
13. `Shape::__iter__`_.
14. `Shape::__setitem__`_.
15. `Shape::__str__`_.

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

.. _Shape::wipe:

**Shape::wipe** (self)

Iterate over the entire canvas and set every square to None.

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

.. _Shape Manipulation:

Shape Manipulation
------------------

Methods
#######

.. _adjoin:

function *adjoin* (shape1, shape2, overlap=0, top_offset=0, fill=None, join_left=False, skip_conflicts=False, collect=False, offset_both=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take two shapes and combine them into one. This method places shapes
side-by-side with ``shape1`` on the left and ``shape2`` on the right. If
``overlap`` is greater than zero, ``shape2`` will overlap ``shape1`` on the
left by ``overlap``. Finally, the resultant shape will be padded using
``fill``.

:``shape1``: The first shape. *Required*.
:``shape2``: The second shape. *Required*.
:``overlap``: How much to overlap ``shape1`` with ``shape2``. *Default*
              *0*.
:``top_offset``: If specified, once the overlap has been calculated, the
                 second shape will be vertically offset by ``top_offset``
                 from the "top" of the canvas. *Default 0*.
:``fill``: The character to pad out the rest of the canvas if
           ``shape1.height() < shape2.height()`` or vice versa.
:``join_left``: If true, will instead join ``shape2`` to the left of
                ``shape1``. This is achieved by swapping the parameters.
                *Default False*.
:``skip_conflicts``: If true and ``overlap`` > 0, will not draw the parts of
                     ``shape2`` where they overlap with the parts of ``shape1``.
:``collect``: If true, returns a ShapeCollection instead of a canvas.
                 *Default False*.
:``offset_both``: If true, the ``top_offset`` will be applied to both
                  shapes. *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _underneath:

function *underneath* (shape1, shape2, left_offset=0, overlap=0, fill=None, join_top=False, skip_conflicts=False, offset_first=False, offset_second=True, collect=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
:``collect``: If true, returns a ShapeCollection instead of a canvas.
                 *Default False*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _atop:

function *atop* (shape1, shape2, left_offset=0, overlap=0, fill=None, join_bottom=False, skip_conflicts=False, offset_first=False, offset_second=True, collect=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
:``collect``: If true, returns a ShapeCollection instead of a canvas.
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
5. `AutoShape::as_shape`_.
6. `AutoShape::height`_.
7. `AutoShape::normalise`_.
8. `AutoShape::size`_.
9. `AutoShape::width`_.
10. `AutoShape::_actual_wrapper`_.
11. `AutoShape::__getitem__`_.
12. `AutoShape::__setitem__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::__init__:

**AutoShape::__init__** (self, fill=None)

Initiate the automatic shape.

:``fill``: What character should be used when normalising the shape.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_height:

**AutoShape::actual_height** (self, \*args, \*\*kwargs)

To compensate for automatic sizing, actual heights of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_size:

**AutoShape::actual_size** (self, \*args, \*\*kwargs)

To compensate for automatic sizing, actual sizes of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::actual_width:

**AutoShape::actual_width** (self, \*args, \*\*kwargs)

To compensate for automatic sizing, actual widths of the AutoShape are
accessed via suffixing "actual" to the function name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AutoShape::as_shape:

**AutoShape::as_shape** (self)

Attempts to convert the current AutoShape into a Shape, and then returns
it.

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

.. _Index:

Index
=====

+---------------------------------+---------------------------------+
|`adjoin`_                        |`atop`_                          |
+---------------------------------+---------------------------------+
|`AutoShape`_                     |`AutoShape::__init__`_           |
+---------------------------------+---------------------------------+
|`AutoShape::actual_height`_      |`AutoShape::actual_size`_        |
+---------------------------------+---------------------------------+
|`AutoShape::actual_width`_       |`AutoShape::as_shape`_           |
+---------------------------------+---------------------------------+
|`AutoShape::height`_             |`AutoShape::normalise`_          |
+---------------------------------+---------------------------------+
|`AutoShape::size`_               |`AutoShape::width`_              |
+---------------------------------+---------------------------------+
|`AutoShape::_actual_wrapper`_    |`AutoShape::__getitem__`_        |
+---------------------------------+---------------------------------+
|`AutoShape::__setitem__`_        |`Box`_                           |
+---------------------------------+---------------------------------+
|`Box::__init__`_                 |`Box::perimeter`_                |
+---------------------------------+---------------------------------+
|`Column`_                        |`Column::__init__`_              |
+---------------------------------+---------------------------------+
|`Shape`_                         |`Shape::__init__`_               |
+---------------------------------+---------------------------------+
|`Shape::column`_                 |`Shape::draw_on`_                |
+---------------------------------+---------------------------------+
|`Shape::height`_                 |`Shape::normalise`_              |
+---------------------------------+---------------------------------+
|`Shape::row`_                    |`Shape::section`_                |
+---------------------------------+---------------------------------+
|`Shape::size`_                   |`Shape::trim`_                   |
+---------------------------------+---------------------------------+
|`Shape::width`_                  |`Shape::wipe`_                   |
+---------------------------------+---------------------------------+
|`Shape::__getitem__`_            |`Shape::__iter__`_               |
+---------------------------------+---------------------------------+
|`Shape::__setitem__`_            |`Shape::__str__`_                |
+---------------------------------+---------------------------------+
|`ShapeColumn`_                   |`ShapeColumn::col`_              |
+---------------------------------+---------------------------------+
|`ShapeColumn::copy`_             |`ShapeColumn::parent`_           |
+---------------------------------+---------------------------------+
|`ShapeColumn::__getitem__`_      |`ShapeColumn::__iter__`_         |
+---------------------------------+---------------------------------+
|`ShapeColumn::__repr__`_         |`ShapeColumn::__setitem__`_      |
+---------------------------------+---------------------------------+
|`ShapeColumn::__str__`_          |`ShapeError`_                    |
+---------------------------------+---------------------------------+
|`ShapeRow`_                      |`ShapeRow::copy`_                |
+---------------------------------+---------------------------------+
|`ShapeRow::parent`_              |`ShapeRow::row`_                 |
+---------------------------------+---------------------------------+
|`ShapeRow::__getitem__`_         |`ShapeRow::__iter__`_            |
+---------------------------------+---------------------------------+
|`ShapeRow::__repr__`_            |`ShapeRow::__setitem__`_         |
+---------------------------------+---------------------------------+
|`ShapeRow::__str__`_             |`underneath`_                    |
+---------------------------------+---------------------------------+