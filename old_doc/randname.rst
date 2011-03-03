
Table of Contents
=================

1. `Random name generation`_

  A. `Utility functions`_

    a. `DatabaseException`_
    b. `coinflip`_
    c. `one_chance_in`_
    d. `check_name_db`_
    e. `db_random_pop_default`_

  B. `Name generation`_

    a. `get_random_male_name`_
    b. `get_random_female_name`_
    c. `get_random_first_name`_
    d. `get_random_lastname_simple`_
    e. `get_random_lastname_nameson`_
    f. `get_random_lastname_irish`_
    g. `get_random_lastname_scottish`_
    h. `get_random_lastname_family`_
    i. `get_random_lastname_combo`_
    j. `get_random_lastname_lowerclass`_
    k. `get_random_lastname_middleclass`_
    l. `get_random_lastname_upperclass`_
    m. `get_random_last_name`_
    n. `get_random_fullname`_

2. `Index`_

.. _Random name generation:

Random name generation
======================

Generate random first, last and full names from various building blocks.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Utility functions:

Utility functions
-----------------

Classes
#######

- `DatabaseException`_.

Methods
#######

.. _DatabaseException:

class *DatabaseException*
^^^^^^^^^^^^^^^^^^^^^^^^^

Exception for non-existing databases.

Methods
#######

1. `DatabaseException::__init__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _DatabaseException::__init__:

**DatabaseException::__init__** (self, value)

Generate the exception.
:``value``: Database name.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _coinflip:

function *coinflip* ()
^^^^^^^^^^^^^^^^^^^^^^

Returns True with a 50% chance, else False.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _one_chance_in:

function *one_chance_in* (n)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns True with a 1/n chance.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _check_name_db:

function *check_name_db* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check whether all needed databases actually exist.
If not, throws an exception.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _db_random_pop_default:

function *db_random_pop_default* (db_name, value=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes a random element from the database and returns it.
If such an element does not exist, returns another value instead.

:``db_value``: Database name.
:``value``: Default return value. *Default None*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Name generation:

Name generation
---------------

Methods
#######

.. _get_random_male_name:

function *get_random_male_name* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random male first name that wasn't picked before.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_female_name:

function *get_random_female_name* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random female first name that wasn't picked before.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_first_name:

function *get_random_first_name* (gender=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random first name that wasn't picked before.

:``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_simple:

function *get_random_lastname_simple* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random simple last name that wasn't picked before.

**Examples**:: Brown, Forrester, Grant, Sheppard, Young.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_nameson:

function *get_random_lastname_nameson* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name ending in "s" or "son".

**Examples**:: Adams, Jackson, Stevenson, Williams.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_irish:

function *get_random_lastname_irish* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name beginning with "O'".

**Examples**:: O'Connor, O'Halloran, O'Neill.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_scottish:

function *get_random_lastname_scottish* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name beginning with "Mc" or "Mac".

**Examples**:: MacCormack, McDonald, MacLeod.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_family:

function *get_random_lastname_family* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name with family associations.

**Examples**:: Adams, Jackson, O'Connor, McDonald, MacLeod.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_combo:

function *get_random_lastname_combo* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name built up of
adjective + noun, or noun + noun.

**Examples**:: Blackstone, Goodfellow, Gladwell, Longbourne.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_lowerclass:

function *get_random_lastname_lowerclass* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused lowerclass last name.

**Examples**:: Brown, Goodfellow, Forrester, Jackson, McCormack, O'Neill.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_middleclass:

function *get_random_lastname_middleclass* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused middleclass last name.

**Examples**:: Goodfellow, Hartlethorpe, Jackson, McCormack, O'Neill.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_lastname_upperclass:

function *get_random_lastname_upperclass* ()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused upperclass last name.
Names get constructed out of a variety of syllables.

**Examples**:: Adderley, Hartlethorpe, Islington, Thistleby, Windermere.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_last_name:

function *get_random_last_name* (style=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random previously unused last name.

:``style``: One of ``'upper'``, ``'middle'`` or ``'lower'`` for
            upper-, middle- and lowerclass names, respectively.
            *Default random*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _get_random_fullname:

function *get_random_fullname* (gender=None, style=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a random full name, consisting of previously unused
first and last names.

:``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
:``style``: One of ``'upper'``, ``'middle'`` or ``'lower'`` for
            upper-, middle- and lowerclass names, respectively.
            *Default random*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+--------------------------------------+--------------------------------------+
|`check_name_db`_                      |`coinflip`_                           |
+--------------------------------------+--------------------------------------+
|`DatabaseException`_                  |`DatabaseException::__init__`_        |
+--------------------------------------+--------------------------------------+
|`db_random_pop_default`_              |`get_random_female_name`_             |
+--------------------------------------+--------------------------------------+
|`get_random_first_name`_              |`get_random_fullname`_                |
+--------------------------------------+--------------------------------------+
|`get_random_lastname_combo`_          |`get_random_lastname_family`_         |
+--------------------------------------+--------------------------------------+
|`get_random_lastname_irish`_          |`get_random_lastname_lowerclass`_     |
+--------------------------------------+--------------------------------------+
|`get_random_lastname_middleclass`_    |`get_random_lastname_nameson`_        |
+--------------------------------------+--------------------------------------+
|`get_random_lastname_scottish`_       |`get_random_lastname_simple`_         |
+--------------------------------------+--------------------------------------+
|`get_random_lastname_upperclass`_     |`get_random_last_name`_               |
+--------------------------------------+--------------------------------------+
|`get_random_male_name`_               |`one_chance_in`_                      |
+--------------------------------------+--------------------------------------+