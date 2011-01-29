
Table of Contents
=================

1. `Colour and style`_

  A. `Colours`_

    a. `BaseColour`_
    b. `Colour`_

  B. `Lists of colours`_

    a. `ColourLibrary`_

2. `Index`_

.. _Colour and style:

Colour and style
================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Colours:

Colours
-------

Classes
#######

- `BaseColour`_.
- `Colour`_.

.. _BaseColour:

class *BaseColour*
^^^^^^^^^^^^^^^^^^

An agnostic representation of a basic, single-state colour, as used by
Urwid.

Methods
#######

1. `BaseColour::__init__`_.
2. `BaseColour::copy`_.
3. `BaseColour::darken`_.
4. `BaseColour::darkened`_.
5. `BaseColour::is_base`_.
6. `BaseColour::lighten`_.
7. `BaseColour::lightened`_.
8. `BaseColour::__cmp__`_.
9. `BaseColour::__rerp__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::__init__:

**BaseColour::__init__** (self, colour_name)

Create a new colour.

:``colour_name``: The representation of the colour.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::copy:

**BaseColour::copy** (self)

Return a copy of the current colour.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::darken:

**BaseColour::darken** (self)

Perform an in-place darkening of the current colour. This function can
only be applied to colours that return True for ``is_base()``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::darkened:

**BaseColour::darkened** (self)

Return a copy of the current colour which has been darkened.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::is_base:

**BaseColour::is_base** (self)

Determines if this colour is a "base colour", that is, one of the 16
"allowed" colours that are defined by Urwid. Colours that are not "base"
are those that are in hexadecimal notation (#fff, for instance)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::lighten:

**BaseColour::lighten** (self)

Performs an in-place lightening of the current colour. This function can
only be currently applied to colours that return True for ``is_base()``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::lightened:

**BaseColour::lightened** (self)

Return a copy of the current colour that has been lightened.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::__cmp__:

**BaseColour::__cmp__** (self, other)

Allow for rich comparison between colours.

:``other``: The colour being compared to. Can either be an instance of
            BaseColour, in which case colour names are compared, or
            Colour, in which case it attempts to compare colour names
            with the Colour's current foreground colour.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::__rerp__:

**BaseColour::__rerp__** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Colour:

class *Colour*
^^^^^^^^^^^^^^

A representation of agnostic colours in a variety of configurations:
individually as either foreground or background colours, combined with
foreground and background colours, individually as a style, or any
combination of the previous with a style.

Methods
#######

1. `Colour::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Colour::__init__:

**Colour::__init__** (self, foreground=None, background=None, style=None)

Create a new colour representation.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Lists of colours:

Lists of colours
----------------

Classes
#######

- `ColourLibrary`_.

.. _ColourLibrary:

class *ColourLibrary*
^^^^^^^^^^^^^^^^^^^^^

A collection of standardised Base colours contained within a specific library.

Methods
#######

1. `ColourLibrary::__init__`_.
2. `ColourLibrary::add`_.
3. `ColourLibrary::find`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ColourLibrary::__init__:

**ColourLibrary::__init__** (self)

Initialise the blank library.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ColourLibrary::add:

**ColourLibrary::add** (self, name, colour=None)

Include a specific colour in the library.

:``name``: The name of the colour.
:``colour``: An instance of BaseColour. If ``None``, a new BaseColour
             will be initialised using ``name`` as the colour name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _ColourLibrary::find:

**ColourLibrary::find** (self, name)

Find a specific colour within the library.

:``name``: The name of the colour being searched for.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+-----------------------------+-----------------------------+
|`BaseColour`_                |`BaseColour::__init__`_      |
+-----------------------------+-----------------------------+
|`BaseColour::copy`_          |`BaseColour::darken`_        |
+-----------------------------+-----------------------------+
|`BaseColour::darkened`_      |`BaseColour::is_base`_       |
+-----------------------------+-----------------------------+
|`BaseColour::lighten`_       |`BaseColour::lightened`_     |
+-----------------------------+-----------------------------+
|`BaseColour::__cmp__`_       |`BaseColour::__rerp__`_      |
+-----------------------------+-----------------------------+
|`Colour`_                    |`Colour::__init__`_          |
+-----------------------------+-----------------------------+
|`ColourLibrary`_             |`ColourLibrary::__init__`_   |
+-----------------------------+-----------------------------+
|`ColourLibrary::add`_        |`ColourLibrary::find`_       |
+-----------------------------+-----------------------------+