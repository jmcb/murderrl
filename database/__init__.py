#!/usr/bin/env python
import sys, os, random

_dbobjects = []

class Database (list):
    """
    An extremely simplistic type that is nothing more than a wrapper on top of
    the default list type.
    """
    def __init__ (self, name, data):
        """
        Initialises the database.

        :``name``: The name of the Database. This is stored and used to describe
                   the database.
        :``data``: The actual data of the Database. This should be a list of
                   items in any format.
        """
        self.name = name
        list.__init__(self, data)
    def copy (self):
        """
        Returns a copy of the database that allows for modification.
        """
        return self.__class__(self.name, self[:])
    def random (self):
        """
        Returns a random element from the Database.
        """
        if len(self) == 0:
            return None
        return random.choice(self)
    def random_pop (self):
        """
        Removes a random element from the Database and then returns it. This is
        an in-place activity.
        """
        if len(self) == 0:
            return None
        item = random.randint(0, len(self))-1
        return self.pop(item)

class WeightedString (str):
    """
    A simple collation of a string and a weight.

    The default weight of ``10`` means that the string has no higher or lesser
    chance of being chosen from a WeightedDatabase than any other string.  A
    weight of ``20`` means that it has double the chance, a weight of ``5``
    meaning that has half the chance, etc.
    """
    def __init__ (self, string, weight=10):
        """
        Create a new weighted string.

        :``string``: The actual string contents.
        :``weight``: The weight of the string. *Default 10*.
        """
        self.weight = weight
        str.__init__(self, string)

class WeightedDatabase (Database):
    """
    A slightly more complicated collection of data stored by weight. The
    "default" weight of the databse is ``10``. Random choices pick things by
    weight as well as randomness, etc.
    """
    def total_weight (self):
        """
        Return the total weight of the database.
        """
        weight = 0
        for item in self:
            assert hasattr(item, "weight")
            weight += item.weight
        return weight

    def random_pick (self):
        """
        Randomly pick an item from the database based on its weight in
        comparison to the total weight of the database. Returns a tuple of
        (``index``, ``item``).
        """
        tweight = self.total_weight()
        n = random.uniform(0, tweight)
        for num, item in enumerate(self):
            if item.weight < n:
                return num, item
            n = n - item.weight

    def random (self):
        """
        Returns a random element from the Database, picked by weight.
        """
        if len(self) == 0:
            return None
        return self.random_pick()[1]

    def random_pop (self):
        """
        Removes a random element from the Database and then returns it. This is
        an in-place activity.
        """
        if len(self) == 0:
            return None
        index = self.random_pick()[0]
        return self.pop(item)

def databases ():
    """
    Returns a list of all Database objects stored.
    """
    return _dbobjects[:]

def database (name):
    """
    Returns a specific Database object. If the Database doesn't exist, will
    instead return ``None``.

    :``name``: The name of the Database object being requested.
    """
    return globals().get(name, None)

def database_exists (name):
    """
    Checks for the existance of a specific database object.

    :``name``: The name of the Database.
    """
    return database(name) is not None

def num_databases ():
    """
    Returns the total number of Databases available.
    """
    return len(_dbobjects)

def _do_build ():
    """
    Convert the contents of the local directory, or a data directory relevant to
    the local directory, into a series of Database objects.
    """
    if os.path.exists("./database"):
        data_path = "./database"
    elif os.path.exists("../database"):
        data_path = "../database"
    elif os.path.exists("../../database"):
        data_path = "../../database"
    else:
        data_path = "."

    databases = [db for db in os.listdir(data_path) if db.endswith(".db")]
    for database in databases:
        # chop the extension off
        name = database[:-3]
        dbfile = open(os.path.join(data_path, database), "r")
        dbdata = [item.strip() for item in dbfile.read().strip().strip("%").split("%")]
        globals()[name] = Database(name, dbdata)
        dbfile.close()
        _dbobjects.append(globals()[name])

if __name__!="__main__":
    _do_build()
