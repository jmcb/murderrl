
Table of Contents
=================

1. `Coord module`_

  A. `Co-ordinates`_

    a. `Coord`_

  B. `Iterators`_

    a. `RectangleIterator`_

  C. `Sizes`_

    a. `Size`_

  D. `Automatic sizes and dimensions`_

    a. `AutoSize`_
    b. `AutoDimension`_

2. `Index`_

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

.. _Index:

Index
=====

+------------------------------+------------------------------+
|`AutoDimension`_              |`AutoSize`_                   |
+------------------------------+------------------------------+
|`AutoSize::__init__`_         |`AutoSize::valid`_            |
+------------------------------+------------------------------+
|`Coord`_                      |`Coord::__init__`_            |
+------------------------------+------------------------------+
|`Coord::as_tuple`_            |`Coord::valid`_               |
+------------------------------+------------------------------+
|`RectangleIterator`_          |`RectangleIterator::__init__`_|
+------------------------------+------------------------------+
|`Size`_                       |`Size::__init__`_             |
+------------------------------+------------------------------+