
Table of Contents
=================

1. `ShapeCollection module`_

  A. `Collections`_

    a. `ShapeCollection`_
    b. `ShapeCoord`_

2. `Index`_

.. _ShapeCollection module:

ShapeCollection module
======================

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
5. `ShapeCollection::extend`_.
6. `ShapeCollection::height`_.
7. `ShapeCollection::offset`_.
8. `ShapeCollection::pop`_.
9. `ShapeCollection::size`_.
10. `ShapeCollection::sort`_.
11. `ShapeCollection::width`_.
12. `ShapeCollection::__getitem__`_.
13. `ShapeCollection::__iter__`_.
14. `ShapeCollection::__len__`_.
15. `ShapeCollection::__setitem__`_.

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

.. _ShapeCollection::extend:

**ShapeCollection::extend** (self, items)

Extends the current collection of ShapeCoords by the passed list of
items.

:``items``: An instance of ShapeCollection. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::height:

**ShapeCollection::height** (self)

Returns the height required to contain each member.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::offset:

**ShapeCollection::offset** (self, offset)

Offsets each member of the ShapeCollection by the passed offset.

:``offset``: A Coord or Size with which to offset each Shape. If this is
             a negative value, the offsetting will be subtractive;
             however, if this results in any ShapeCoord being negatively
             offset, an error will be raised, and the offsetting will be
             abandoned. *Required*.

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

.. _Index:

Index
=====

+------------------------------------+------------------------------------+
|`ShapeCollection`_                  |`ShapeCollection::__init__`_        |
+------------------------------------+------------------------------------+
|`ShapeCollection::append`_          |`ShapeCollection::combine`_         |
+------------------------------------+------------------------------------+
|`ShapeCollection::copy`_            |`ShapeCollection::extend`_          |
+------------------------------------+------------------------------------+
|`ShapeCollection::height`_          |`ShapeCollection::offset`_          |
+------------------------------------+------------------------------------+
|`ShapeCollection::pop`_             |`ShapeCollection::size`_            |
+------------------------------------+------------------------------------+
|`ShapeCollection::sort`_            |`ShapeCollection::width`_           |
+------------------------------------+------------------------------------+
|`ShapeCollection::__getitem__`_     |`ShapeCollection::__iter__`_        |
+------------------------------------+------------------------------------+
|`ShapeCollection::__len__`_         |`ShapeCollection::__setitem__`_     |
+------------------------------------+------------------------------------+
|`ShapeCoord`_                       |`ShapeCoord::height`_               |
+------------------------------------+------------------------------------+
|`ShapeCoord::size`_                 |`ShapeCoord::width`_                |
+------------------------------------+------------------------------------+