#!/usr/bin/env python
"""
Generate random first, last and full names from various building blocks.
"""

import random, sys

import database.database as db
from library.random_util import *

class DatabaseException (Exception):
    """
    Exception for non-existing databases.
    """
    def __init__(self, value):
        """
        Generate the exception.
        :``value``: Database name.
        """
        self.value = value
    def __str__(self):
        return repr("Database '%s' does not exist" % self.value)

##################################################
# Database files: ../database/names.db/<file>.db

DB_FIRST_MALE   = 'names.first_male'
DB_FIRST_FEMALE = 'names.first_female'
DB_LAST_SIMPLE  = 'names.last_simple'
DB_LAST_NAMESON = 'names.last_nameson'
DB_LAST_GAELIC1 = 'names.last_gaelic1'
DB_LAST_GAELIC2 = 'names.last_gaelic2'
DB_LAST_COMBO1  = 'names.last_combo1'
DB_LAST_COMBO2  = 'names.last_combo2'
DB_LAST_UPPER1  = 'names.last_upperclass1'
DB_LAST_UPPER2  = 'names.last_upperclass2'
DB_LAST_UPPER3  = 'names.last_upperclass3'
DB_LAST_UPPER4  = 'names.last_upperclass4'

def check_name_db ():
    """
    Check whether all needed databases actually exist.
    If not, throws an exception.
    """
    db_checks = [DB_FIRST_MALE, DB_FIRST_FEMALE,
                 DB_LAST_SIMPLE, DB_LAST_NAMESON,
                 DB_LAST_GAELIC1, DB_LAST_GAELIC2,
                 DB_LAST_COMBO1, DB_LAST_COMBO2,
                 DB_LAST_UPPER1, DB_LAST_UPPER2]

    db_exists = db.database_exists
    for db_name in db_checks:
        if not db_exists(db_name):
            raise DatabaseException, db_name

##################################################
# Name generation methods
def db_random_pop_default (db_name, value = None):
    """
    Removes a random element from the database and returns it.
    If such an element does not exist, returns another value instead.

    :``db_value``: Database name.
    :``value``: Default return value. *Default None*
    """
    name = db.get_database(db_name).random_pop()
    if not name:
        if not value:
            return get_random_lastname_simple()
        else:
            return value
    return name

def get_random_male_name ():
    """
    Returns a random male first name that wasn't picked before.
    """
    return db_random_pop_default(DB_FIRST_MALE, "John")

def get_random_female_name ():
    """
    Returns a random female first name that wasn't picked before.
    """
    return db_random_pop_default(DB_FIRST_FEMALE, "Jane")

def get_random_first_name (gender = None):
    """
    Returns a random first name that wasn't picked before.

    :``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
    """
    if not gender:
        gender = random.choice(('f', 'm'))

    if gender == 'f':
        return get_random_female_name()
    else:
        return get_random_male_name()

#################################################
# Surnames
def get_random_lastname_simple ():
    """
    Returns a random simple last name that wasn't picked before.

    **Examples**:: Brown, Forrester, Grant, Sheppard, Young.
    """
    return db_random_pop_default(DB_LAST_SIMPLE, "Doe")

def get_random_lastname_nameson ():
    """
    Returns a random previously unused last name ending in "s" or "son".

    **Examples**:: Adams, Jackson, Stevenson, Williams.
    """
    name = db.get_database(DB_LAST_NAMESON).random_pop()
    if not name:
        return get_random_lastname_simple()
    if name.endswith('s'):
        if coinflip():
            return name
        else:
            return "%son" % name
    return "%sson" % name

def get_random_lastname_irish ():
    """
    Returns a random previously unused last name beginning with "O'".

    **Examples**:: O'Connor, O'Halloran, O'Neill.
    """
    name = db.get_database(DB_LAST_GAELIC1).random_pop()
    if not name:
        return get_random_lastname_simple()
    return "O'%s" % name

def get_random_lastname_scottish ():
    """
    Returns a random previously unused last name beginning with "Mc" or "Mac".

    **Examples**:: MacCormack, McDonald, MacLeod.
    """
    name = db.get_database(DB_LAST_GAELIC2).random_pop()
    if not name:
        return get_random_lastname_simple()
    return "%s%s" % (random.choice(('Mc', 'Mac')), name)

def get_random_lastname_family ():
    """
    Returns a random previously unused last name with family associations.

    **Examples**:: Adams, Jackson, O'Connor, McDonald, MacLeod.
    """
    if one_chance_in(3):
        return get_random_lastname_irish ()
    elif coinflip():
        return get_random_lastname_scottish ()
    else:
        return get_random_lastname_nameson()

def get_random_lastname_combo ():
    """
    Returns a random previously unused last name built up of
    adjective + noun, or noun + noun.

    **Examples**:: Blackstone, Goodfellow, Gladwell, Longbourne.
    """
    first = db.get_database(DB_LAST_COMBO1).random_pop()
    if not first:
        return get_random_lastname_simple()

    second = db.get_database(DB_LAST_COMBO2).random_pop()
    if not second:
        return get_random_lastname_simple()

    if second[0] == 'w' and first.endswith('w'):
        second = second[1:]
    return "%s%s" % (first, second)

def get_random_lastname_lowerclass ():
    """
    Returns a random previously unused lowerclass last name.

    **Examples**:: Brown, Goodfellow, Forrester, Jackson, McCormack, O'Neill.
    """
    if one_chance_in(5):
        return get_random_lastname_combo()
    elif coinflip():
        return get_random_lastname_simple()
    else:
        return get_random_lastname_family()

def get_random_lastname_middleclass ():
    """
    Returns a random previously unused middleclass last name.

    **Examples**:: Goodfellow, Hartlethorpe, Jackson, McCormack, O'Neill.
    """
    if one_chance_in(8):
        return get_random_lastname_upperclass()
    elif one_chance_in(6):
        return get_random_lastname_simple()
    elif one_chance_in(2):
        return get_random_lastname_family()
    else:
        return get_random_lastname_combo()

def get_random_lastname_upperclass ():
    """
    Returns a random previously unused upperclass last name.
    Names get constructed out of a variety of syllables.

    **Examples**:: Adderley, Hartlethorpe, Islington, Thistleby, Windermere.
    """
    first  = db.get_database(DB_LAST_UPPER1).random_pop()
    second = db.get_database(DB_LAST_UPPER2).random_pop()
    third  = db.get_database(DB_LAST_UPPER3).random()
    fourth = db.get_database(DB_LAST_UPPER4).random_pop()
    if not (first and second and third and fourth):
        return get_random_lastname_middleclass()

    return "%s%s%s%s" % (first, second, third, fourth)

def get_random_last_name (style = None):
    """
    Returns a random previously unused last name.

    :``style``: One of ``'upper'``, ``'middle'`` or ``'lower'`` for
                upper-, middle- and lowerclass names, respectively.
                *Default random*.
    """
    styles = ['upper', 'middle', 'lower']
    if not style:
        style = random.choice(styles)

    if style in ('u', 'up', 'upper', 'upperclass'):
        name = get_random_lastname_upperclass()
    elif style in ('l', 'low', 'lower', 'lowerclass'):
        name = get_random_lastname_lowerclass()
    else:
        name = get_random_lastname_middleclass()

    if not name:
        return get_random_lastname_simple()
    else:
        return name

def get_random_fullname(gender = None, style = None):
    """
    Returns a random full name, consisting of previously unused
    first and last names.

    :``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
    :``style``: One of ``'upper'``, ``'middle'`` or ``'lower'`` for
                upper-, middle- and lowerclass names, respectively.
                *Default random*.
    """
    firstname = get_random_first_name(gender)
    lastname  = get_random_last_name(style)
    return "%s %s" % (firstname, lastname)
