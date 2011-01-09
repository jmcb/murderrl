
Table of Contents
=================

1. `Documentation parser`_

  A. `Classes`_

    a. `Document`_
    b. `Module`_
    c. `Section`_

  B. `Methods`_

    a. `docparser`_

2. `Index`_

.. _Documentation parser:

Documentation parser
====================

docparser, a quick parser for documentation configuration.

This converts a flat representation of what methods and classes of what modules
should be documented, and in which sections, from text into an iterable
document. The file format for \*.conf files allows combinations of the following
signifiers:

:`$ignore`_: ``qualified name``
:`$search`_: ``path1``, ``path2``, ...
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

.. _$search:

``$search``:
------------

Arguments: 

:[``path1``, ``path2``, ...]: A string of comma-separated search paths.

``$search`` allows you to specify additional paths that should be searched when
importing modules. These can be absolute paths of relative directories, but they
must each exist.

If ``$search`` is provided, it should be the first line of the document,
otherwise the actual parser will fail to properly import modules.

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

+-------------------------+-------------------------+
|`docparser`_             |`Document`_              |
+-------------------------+-------------------------+
|`Document::__iter__`_    |`Document::__str__`_     |
+-------------------------+-------------------------+
|`Module`_                |`Module::__init__`_      |
+-------------------------+-------------------------+
|`Section`_               |`Section::__init__`_     |
+-------------------------+-------------------------+