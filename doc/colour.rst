
Table of Contents
=================

1. `Colour and style`_

  A. `Colours`_

    a. `BaseColour`_
    b. `Colour`_

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
2. `BaseColour::is_base`_.
3. `BaseColour::__rerp__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::__init__:

**BaseColour::__init__** (self, colour_name)

Create a new colour.

:``colour_name``: The representation of the colour.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BaseColour::is_base:

**BaseColour::is_base** (self)

Determines if this colour is a "base colour", that is, one of the 16
"allowed" colours that are defined by Urwid. Colours that are not "base"
are those that are in hexadecimal notation (#fff, for instance)

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

.. _Index:

Index
=====

+---------------------------+---------------------------+
|`BaseColour`_              |`BaseColour::__init__`_    |
+---------------------------+---------------------------+
|`BaseColour::is_base`_     |`BaseColour::__rerp__`_    |
+---------------------------+---------------------------+
|`Colour`_                  |`Colour::__init__`_        |
+---------------------------+---------------------------+