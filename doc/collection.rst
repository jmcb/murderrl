
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
3. `ShapeCollection::column`_.
4. `ShapeCollection::combine`_.
5. `ShapeCollection::copy`_.
6. `ShapeCollection::draw_on`_.
7. `ShapeCollection::extend`_.
8. `ShapeCollection::height`_.
9. `ShapeCollection::insert`_.
10. `ShapeCollection::offset`_.
11. `ShapeCollection::place_on`_.
12. `ShapeCollection::pop`_.
13. `ShapeCollection::prioritise`_.
14. `ShapeCollection::reverse`_.
15. `ShapeCollection::reversed`_.
16. `ShapeCollection::row`_.
17. `ShapeCollection::size`_.
18. `ShapeCollection::sort`_.
19. `ShapeCollection::width`_.
20. `ShapeCollection::__getitem__`_.
21. `ShapeCollection::__iter__`_.
22. `ShapeCollection::__len__`_.
23. `ShapeCollection::__setitem__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::__init__:

**ShapeCollection::__init__** (self, shapes=None)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::append:

**ShapeCollection::append** (self, item, c=None)

As with the initialisation function, all Shapes passed in are here
converted into ShapeCoords, using Coord(0, 0) as their offset. All other
instances are not allowed.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::column:

**ShapeCollection::column** (self, column)

Provides an iteration of CollectionCoords.

:``column``: Which column you want to iterate over.

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

.. _ShapeCollection::draw_on:

**ShapeCollection::draw_on** (self, target, offset=None)

Via direct canvas access, draws the contents of ``shape`` onto the
relevant spots of each canvas contained within.

``target``: The shape that should be drawn on this collection.
``offset``: A Coord denoting by how much the shape should be offset
            before drawing. *Default None*

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

.. _ShapeCollection::insert:

**ShapeCollection::insert** (self, index, item)

Insert ``item`` at ``index``, shifting contents down by one. If the
index is beyond the bounds of the collection, it will be appended
instead.

Returns the index that the item was actually inserted at.

:``index``: What index to insert the item at.
:``item``: The shape to insert.

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

.. _ShapeCollection::place_on:

**ShapeCollection::place_on** (self, new_collection, offset=None)

Offset the contents of ``new_collection`` by ``offset`` and then extend
this collection with the contents of ``new_collection``.

``new_collection``: An instance of ShapeCollection, or one of its
                    subclasses.
``offset``: A Coord denoting by how much the ``new_collection`` should
            be offset. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::pop:

**ShapeCollection::pop** (self, index=-1)

Pop index ``index`` item from the collection of ShapeCoords.

:``index``: The index in question. *Default -1*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::prioritise:

**ShapeCollection::prioritise** (self, index, priority=True)

Alter the priority of ``index``. Priority basically equates to the
location within the ShapeCollection: indexes with a higher priority are
drawn later and are thus less likely to be overriden by another shape;
likewise, indexes with lower priorities are drawn earlier and a thus
more likely to be override by another shape.

Priorities are only as valid as long as new items are not added to the
collection.

Returns the new index of the item.

:``index``: The index you wish to prioritise.
:``priority``: The priority you want to set the index to. Negative
               numbers will decrease the priority, and positive numbers
               increase it. If True, the priority will be increased to
               as high as possible. If False, it will be decreased to as
               low as possible. *Default True*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::reverse:

**ShapeCollection::reverse** (self)

Performs an in-place reversing of the contents of this ShapeCollection.
This has the effect of reversing the priority: items added earlier will
be drawn later, and vice versa. For example::

  >> coll = ShapeCollection()
  >> coll.append(Shape(3, 3, "Y"))
  >> coll.append(Shape(3, 3, "X"))

Combining this will result in::

  >> print coll.combine()
  XXX
  XXX
  XXX

Calling reverse before combining results in:

  >> coll.reverse()
  >> print coll.combine()
  YYY
  YYY
  YYY

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::reversed:

**ShapeCollection::reversed** (self)

Returns a copy of this collection that has been reversed. See
``ShapeCollection::reverse``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ShapeCollection::row:

**ShapeCollection::row** (self, row)

Provides an iteration of CollectionCoords.

:``row``: Which row you want to iterate over.

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

If ``item`` is an integer:

Fetch item index ``item`` from the collection of ShapeCoords.

If ``item`` is a Coord instance:

Attempt to locate ``item`` in the contained ShapeCoords. If ``item`` is
contained within multiple shapes, a list of them will be returned.

:``item``: The item to be fetched. Either an integer or a Coord.

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

If ``item`` is an integer:

Insert ``value`` at ``item``, replacing whatever ShapeCoord is existent
there.

:``item``: The index the value is to be inserted at.
:``value``: The value to be inserted. This is automatically cased
            from a Shape into a ShapeCoord(Shape, Coord(0, 0)).
            Otherwise it is assumed to be a ShapeCoord. All other
            types will cause an error.

If ``item`` is an instance of Coord:

Insert ``value`` at ``item`` in each Shape contained within. If ``item``
is found in multiple shapes, it will set ``value`` in each one; if
``value`` is iterable and multiple instances are found, values will be
applied from ``value[0]`` onwards. If it runs out of values in
``value``, it will cease setting and return.

:``item``: Instance of Coord.
:``value``: Either one of or a list of width one strings.

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
|`ShapeCollection::append`_          |`ShapeCollection::column`_          |
+------------------------------------+------------------------------------+
|`ShapeCollection::combine`_         |`ShapeCollection::copy`_            |
+------------------------------------+------------------------------------+
|`ShapeCollection::draw_on`_         |`ShapeCollection::extend`_          |
+------------------------------------+------------------------------------+
|`ShapeCollection::height`_          |`ShapeCollection::insert`_          |
+------------------------------------+------------------------------------+
|`ShapeCollection::offset`_          |`ShapeCollection::place_on`_        |
+------------------------------------+------------------------------------+
|`ShapeCollection::pop`_             |`ShapeCollection::prioritise`_      |
+------------------------------------+------------------------------------+
|`ShapeCollection::reverse`_         |`ShapeCollection::reversed`_        |
+------------------------------------+------------------------------------+
|`ShapeCollection::row`_             |`ShapeCollection::size`_            |
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