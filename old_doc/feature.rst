
Table of Contents
=================

1. `Feature representations`_

  A. `Features`_

    a. `Feature`_
    b. `TextFeature`_

2. `Index`_

.. _Feature representations:

Feature representations
=======================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Features:

Features
--------

Classes
#######

- `Feature`_.

 - `TextFeature`_.


.. _Feature:

class *Feature*
^^^^^^^^^^^^^^^

A way of representing a specific feature in an agnostic manner. This should
be subclassed for the different interfaces, never used directly.

Methods
#######

1. `Feature::__init__`_.
2. `Feature::description`_.
3. `Feature::name`_.
4. `Feature::traversable`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Feature::__init__:

**Feature::__init__** (self, name, description, traversable=False)

Create a new feature. 

:``name``: The name of the feature, which will be used when describing the
           feature upon examination.
:``description``: This string value will be used to describe the feature
           upon examination.
:``traversable``: If True, this glyph is traversable.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Feature::description:

**Feature::description** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Feature::name:

**Feature::name** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Feature::traversable:

**Feature::traversable** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _TextFeature:

class *TextFeature*
^^^^^^^^^^^^^^^^^^^

A representation of an agnostic ``Feature`` as text. This includes a
variety of symbols and colours.

Methods
#######

1. `TextFeature::__init__`_.
2. `TextFeature::colour`_.
3. `TextFeature::glyph`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _TextFeature::__init__:

**TextFeature::__init__** (self, glyph=None, colour=None, name='', description='', traversable=False)

Create a new TextFeature.

:``glyph``: The glyph used to represent this feature.
:``colour``: The colour used to colour this feature. Should be an
             instance of Colour.
:``name``: The name of this feature.
:``description``: The description of this feature.
:``traversable``: Whether or not this glyph can be traversed by the
                  player or non-player characters.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _TextFeature::colour:

**TextFeature::colour** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _TextFeature::glyph:

**TextFeature::glyph** (self)

*Method undocumented*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+----------------------------+----------------------------+
|`Feature`_                  |`Feature::__init__`_        |
+----------------------------+----------------------------+
|`Feature::description`_     |`Feature::name`_            |
+----------------------------+----------------------------+
|`Feature::traversable`_     |`TextFeature`_              |
+----------------------------+----------------------------+
|`TextFeature::__init__`_    |`TextFeature::colour`_      |
+----------------------------+----------------------------+