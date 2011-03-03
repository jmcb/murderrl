
Table of Contents
=================

1. `Database module`_

  A. `Flat-text database`_

    a. `Database`_
    b. `get_databases`_
    c. `get_database`_
    d. `database_exists`_
    e. `num_databases`_

  B. `Weighted databases`_

    a. `WeightedString`_
    b. `WeightedDatabase`_

  C. `Database specifications and related`_

    a. `split_escaped_delim`_
    b. `parse_spec`_
    c. `build_from_file_name`_

2. `Index`_

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

function *get_database* (name, parent=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a specific Database object. If the Database doesn't exist, will
instead return ``None``.

:``name``: The name of the Database object being requested.
:``parent``: A possible DatabaseFolder instance or name to be searched
             instead of the global scope. *Default None*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _database_exists:

function *database_exists* (name, parent=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Checks for the existance of a specific database object.

:``name``: The name of the Database.
:``parent``: A possible DatabaseFolder instance or name to be searched
             instead of the global scope. *Default None*.

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

.. _Database specifications and related:

Database specifications and related
-----------------------------------

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

.. _build_from_file_name:

function *build_from_file_name* (database, data_path, folder=None, spec=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Converts a database file via a specification into a Database instance and
then inserts into into the global scope or a specific parent based on
provided information.

:``database``: The filename to be opened. If this is in a subfolder, the
               subfolder name will be removed from the final name and the
               database will be available globally, unless ``folder`` has
               been specified, or ``folder`` is already a globally available
               folder. *Required*.
:``data_path``: This will be appended to the beginning of all I/O operations
                but will not be treated as a ``folder``. *Required*.
:``folder``: The folder this database will be appended to. If None and the
             database contains a folder name, the folder will be looked for
             globally and if found, the database will be appended to this;
             if there is no folder available, the database will be inserted
             into the global scope. *Default None*.
:``spec``: A specification object that matches the contents of this
           database. If not provided, and a specification exists, this
           specification will be used instead. If not provided and ``folder``
           is not none, and the ``folder`` contains a specification, this
           will be used instead. *Default None*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+-------------------------------------+-------------------------------------+
|`build_from_file_name`_              |`Database`_                          |
+-------------------------------------+-------------------------------------+
|`Database::__init__`_                |`Database::copy`_                    |
+-------------------------------------+-------------------------------------+
|`Database::random`_                  |`Database::random_pop`_              |
+-------------------------------------+-------------------------------------+
|`database_exists`_                   |`get_database`_                      |
+-------------------------------------+-------------------------------------+
|`get_databases`_                     |`num_databases`_                     |
+-------------------------------------+-------------------------------------+
|`parse_spec`_                        |`split_escaped_delim`_               |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase`_                  |`WeightedDatabase::random`_          |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase::random_pick`_     |`WeightedDatabase::random_pop`_      |
+-------------------------------------+-------------------------------------+
|`WeightedDatabase::total_weight`_    |`WeightedString`_                    |
+-------------------------------------+-------------------------------------+