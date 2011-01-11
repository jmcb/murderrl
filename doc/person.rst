
Table of Contents
=================

1. `Peeople and suspect module`_

  A. `People`_

    a. `Person`_
    b. `SuspectList`_

2. `Index`_

.. _Peeople and suspect module:

Peeople and suspect module
==========================

Set up characters, their basic traits and relationships.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _People:

People
------

Classes
#######

- `Person`_.
- `SuspectList`_.

.. _Person:

class *Person*
^^^^^^^^^^^^^^

Person class. To define persons and access their characteristics.

Methods
#######

1. `Person::__init__`_.
2. `Person::chance_of_children`_.
3. `Person::chance_of_spouse`_.
4. `Person::check_has_relative`_.
5. `Person::create_child`_.
6. `Person::create_spouse`_.
7. `Person::describe`_.
8. `Person::describe_relations`_.
9. `Person::get_fullname`_.
10. `Person::get_mirrored_gender`_.
11. `Person::get_name`_.
12. `Person::get_relative`_.
13. `Person::has_children`_.
14. `Person::is_married`_.
15. `Person::is_servant`_.
16. `Person::set_random_age`_.
17. `Person::set_random_hair_colour`_.
18. `Person::set_random_last_name`_.
19. `Person::set_relative`_.
20. `Person::__str__`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::__init__:

**Person::__init__** (self, role='ROLE_GUEST', gender=None, last=None, age=None)

Initialize a new person.

:``role``: One of ``ROLE_OWNER``, ``ROLE_FAMILY``, ``ROLE_GUEST`` or ``ROLE_SERVANT``. *Default ``ROLE_GUEST``*.
           The role influences the choice of surname, age, and honorifics.
:``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
:``last``: Last name. *Default random*.
:``age``: Age. *Default random*.

In addition, the hair colour is randomly chosen.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::chance_of_children:

**Person::chance_of_children** (self)

Returns True if we should generate children.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::chance_of_spouse:

**Person::chance_of_spouse** (self)

Returns True if we should generate a spouse.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::check_has_relative:

**Person::check_has_relative** (self, type)

Returns whether a given relationship type exists for this
person.

:``type``: The type of the relationship: ``REL_SPOUSE``,
           ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::create_child:

**Person::create_child** (self)

Generates a child for the current person.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::create_spouse:

**Person::create_spouse** (self)

Generates a husband or wife for the current person.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::describe:

**Person::describe** (self, list)

Prints the person's description and lists their relationships.

:``list``: An object of type SuspectList. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::describe_relations:

**Person::describe_relations** (self, list)

Prints a listing of this person's relatives.

:``list``: An object of type SuspectList. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::get_fullname:

**Person::get_fullname** (self)

Returns a person's full name, including titles.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::get_mirrored_gender:

**Person::get_mirrored_gender** (self)

Returns the opposite gender to the current person one's.
Used to decide spouses' genders.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::get_name:

**Person::get_name** (self)

Returns a person's full name, excluding titles.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::get_relative:

**Person::get_relative** (self, type)

Returns the first relative (suspects[] index) that matches a
given relationship type. Only really makes sense for binary
relationships, i.e. spouses or fiances.

:``type``: The type of the relationship: ``REL_SPOUSE``,
           ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::has_children:

**Person::has_children** (self)

Returns whether a person has children.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::is_married:

**Person::is_married** (self)

Returns whether a person is married.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::is_servant:

**Person::is_servant** (self)

Returns whether a person is part of the staff.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::set_random_age:

**Person::set_random_age** (self, age=None)

Sets a person's appropriate age depending on their role.

:``age``: Age. *Default random*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::set_random_hair_colour:

**Person::set_random_hair_colour** (self)

Assigns a random hair colour.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::set_random_last_name:

**Person::set_random_last_name** (self, last=None)

Sets a person's appropriate last name (upperclass, middleclass,
lowerclass) depending on their role.

:``last``: Last name. *Default random*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::set_relative:

**Person::set_relative** (self, idx, type)

Add a relative to this person's relationship list.
Requires suspects[] index and relationship type
('spouse', 'parent', 'child', 'engaged').

:``idx``: The current person's index in the suspect list. *Required*.
:``type``: The type of the relationship: ``REL_SPOUSE``,
           ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Person::__str__:

**Person::__str__** (self)

Prints a single-line description of the person.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList:

class *SuspectList*
^^^^^^^^^^^^^^^^^^^

A representation of all suspects, in form of a list of Persons
and the indices of victim and murderer.

Methods
#######

1. `SuspectList::__init__`_.
2. `SuspectList::add_child`_.
3. `SuspectList::add_honorifics`_.
4. `SuspectList::add_occupation`_.
5. `SuspectList::add_relatives`_.
6. `SuspectList::add_spouse`_.
7. `SuspectList::ensure_unique_names`_.
8. `SuspectList::get_murderer`_.
9. `SuspectList::get_suspect`_.
10. `SuspectList::get_suspect_list`_.
11. `SuspectList::get_victim`_.
12. `SuspectList::is_murderer`_.
13. `SuspectList::is_victim`_.
14. `SuspectList::no_of_suspects`_.
15. `SuspectList::pick_murderer`_.
16. `SuspectList::pick_victim`_.
17. `SuspectList::print_suspects`_.
18. `SuspectList::real_no_of_suspects`_.
19. `SuspectList::update_child`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::__init__:

**SuspectList::__init__** (self, max_suspects)

As long as more suspects are needed, generate new persons
and, in another loop, also their relatives.

:``max_suspects``: The maximum number of suspects. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::add_child:

**SuspectList::add_child** (self, parent_idx)

Generates a child for a given person, and sets the necessary
relationship.

:``idx``: The current person's index in the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::add_honorifics:

**SuspectList::add_honorifics** (self)

Add honorifics to some of the suspects, as befits their role.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::add_occupation:

**SuspectList::add_occupation** (self)

Add occupations for the staff, and also to some of the other
suspects, as befits their role.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::add_relatives:

**SuspectList::add_relatives** (self, role, max_persons, count)

Given the current index (count), generates more persons
related to the people already in the sub-list suspects[count:].

:``role``: One of ``ROLE_OWNER``, ``ROLE_FAMILY``, ``ROLE_GUEST``
           or ``ROLE_SERVANT``. *Required*.
:``max_persons``: The maximum total number of suspects. *Required*.
:``count``: The index of the first person to begin the iteration
            over the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::add_spouse:

**SuspectList::add_spouse** (self, idx)

Generates a husband or wife for a given person, and sets the
necessary relationship.

:``idx``: The index of the current person in the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::ensure_unique_names:

**SuspectList::ensure_unique_names** (self)

Reroll names that start with the same letters as names already
in the list. This greatly reduces the danger of the player
getting the characters mixed up.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::get_murderer:

**SuspectList::get_murderer** (self)

Returns the murderer in form of a Person object.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::get_suspect:

**SuspectList::get_suspect** (self, idx)

Returns a Person object matching the given index in the
suspects[] list.

:``idx``: An index of the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::get_suspect_list:

**SuspectList::get_suspect_list** (self)

Returns the suspects list of type Person[].

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::get_victim:

**SuspectList::get_victim** (self)

Returns the victim in form of a Person object.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::is_murderer:

**SuspectList::is_murderer** (self, idx)

Returns True if the given index matches the murderer.

:``idx``: An index of the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::is_victim:

**SuspectList::is_victim** (self, idx)

Returns True if the given index matches the victim.

:``idx``: An index of the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::no_of_suspects:

**SuspectList::no_of_suspects** (self)

Returns the length of the suspects list.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::pick_murderer:

**SuspectList::pick_murderer** (self)

Randomly pick the murderer.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::pick_victim:

**SuspectList::pick_victim** (self)

Randomly pick the victim. Staff are excluded.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::print_suspects:

**SuspectList::print_suspects** (self)

Prints the complete list of suspects and their relationships.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::real_no_of_suspects:

**SuspectList::real_no_of_suspects** (self)

Returns the real number of suspects, i.e. excludes the victim.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _SuspectList::update_child:

**SuspectList::update_child** (self, idx_parent, idx_child)

Updates relationship and age range for a parent and child,
passed as indices.

:``idx_parent``: The parent's index in the suspects[] list. *Required*.
:``idx_child``: The child's index in the suspects[] list. *Required*.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Index:

Index
=====

+----------------------------------------+----------------------------------------+
|`Person`_                               |`Person::__init__`_                     |
+----------------------------------------+----------------------------------------+
|`Person::chance_of_children`_           |`Person::chance_of_spouse`_             |
+----------------------------------------+----------------------------------------+
|`Person::check_has_relative`_           |`Person::create_child`_                 |
+----------------------------------------+----------------------------------------+
|`Person::create_spouse`_                |`Person::describe`_                     |
+----------------------------------------+----------------------------------------+
|`Person::describe_relations`_           |`Person::get_fullname`_                 |
+----------------------------------------+----------------------------------------+
|`Person::get_mirrored_gender`_          |`Person::get_name`_                     |
+----------------------------------------+----------------------------------------+
|`Person::get_relative`_                 |`Person::has_children`_                 |
+----------------------------------------+----------------------------------------+
|`Person::is_married`_                   |`Person::is_servant`_                   |
+----------------------------------------+----------------------------------------+
|`Person::set_random_age`_               |`Person::set_random_hair_colour`_       |
+----------------------------------------+----------------------------------------+
|`Person::set_random_last_name`_         |`Person::set_relative`_                 |
+----------------------------------------+----------------------------------------+
|`Person::__str__`_                      |`SuspectList`_                          |
+----------------------------------------+----------------------------------------+
|`SuspectList::__init__`_                |`SuspectList::add_child`_               |
+----------------------------------------+----------------------------------------+
|`SuspectList::add_honorifics`_          |`SuspectList::add_occupation`_          |
+----------------------------------------+----------------------------------------+
|`SuspectList::add_relatives`_           |`SuspectList::add_spouse`_              |
+----------------------------------------+----------------------------------------+
|`SuspectList::ensure_unique_names`_     |`SuspectList::get_murderer`_            |
+----------------------------------------+----------------------------------------+
|`SuspectList::get_suspect`_             |`SuspectList::get_suspect_list`_        |
+----------------------------------------+----------------------------------------+
|`SuspectList::get_victim`_              |`SuspectList::is_murderer`_             |
+----------------------------------------+----------------------------------------+
|`SuspectList::is_victim`_               |`SuspectList::no_of_suspects`_          |
+----------------------------------------+----------------------------------------+
|`SuspectList::pick_murderer`_           |`SuspectList::pick_victim`_             |
+----------------------------------------+----------------------------------------+
|`SuspectList::print_suspects`_          |`SuspectList::real_no_of_suspects`_     |
+----------------------------------------+----------------------------------------+