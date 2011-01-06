#!/usr/bin/env python
import sys, os, random, collections, re

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
    def random (self, checkfn=None):
        """
        Returns a random element from the Database.

        :``checkfn``: A function to be applied to results. If this function
                      returns ``true``, the result is allowed; if it returns
                      ``false``, another item is picked. *Default None*.
        """
        if len(self) == 0:
            return None
        if checkfn is None:
            return random.choice(self)
        else:
            item = random.choice(self)
            tries = len(self) * 5
            while not checkfn(item):
                item = random.choice(self)
                tries = tries - 1
                if tries <= 0:
                    return None
            return item
    def random_pop (self, checkfn=None):
        """
        Removes a random element from the Database and then returns it. This is
        an in-place activity.

        :``checkfn``: A function to be applied to results. If this function
                      returns ``true``, the result is allowed; if it returns
                      ``false``, another item is picked. *Default None*.
        """
        if len(self) == 0:
            return None
        item = random.randint(0, len(self)-1)
        if checkfn is not None:
            tries = len(self) * 5
            while not checkfn(self[item]):
                item = random.randint(0, len(self)-1)
                tries = tries - 1
                if tries <= 0:
                    return None
        return self.pop(item)
    def __repr__ (self):
        return "Database[%s]" % (list.__repr__(self))

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
    def total_weight (self, checkfn=None):
        """
        Return the total weight of the database.

        :``checkfn``: A function to be applied to each item. If the function
                      returns ``false``, the weight of the item is ignored (and the
                      item is discarded). *Default None*.
        """
        weight = 0
        for item in self:
            if checkfn is not None and not checkfn(item):
                continue
            assert hasattr(item, "weight")
            weight += item.weight
        return weight

    def random_pick (self, checkfn=None):
        """
        Randomly pick an item from the database based on its weight in
        comparison to the total weight of the database. Returns a tuple of
        (``index``, ``item``).

        :``checkfn``: A function to be applied to the items in the database: if
                      it returns ``false``, the item is not considered. *Default
                      None*.
        """
        tweight = self.total_weight(checkfn=checkfn)
        if tweight == 0:
            return None, None
        n = random.uniform(0, tweight)
        for num, item in enumerate(self):
            if checkfn is not None and not checkfn(item):
                continue

            if item.weight < n:
                return num, item
            n = n - item.weight

    def random (self, checkfn=None):
        """
        Returns a random element from the Database, picked by weight.

        :``checkfn``: A function to be applied to the items in the database: if
                      it returns ``false``, the item is not considered. *Default
                      None*.
        """
        if len(self) == 0:
            return None
        return self.random_pick(checkfn=checkfn)[1]

    def random_pop (self, checkfn=None):
        """
        Removes a random element from the Database and then returns it. This is
        an in-place activity.

        :``checkfn``: A function to be applied to the items in the database: if
                      it returns ``false``, the item is not considered. *Default
                      None*.
        """
        if len(self) == 0:
            return None

        index = self.random_pick(checkfn=checkfn)[0]

        if index == None:
            return None

        return self.pop(item)

    def __repr__ (self):
        return "WeightedDatabase[%s]" % (list.__repr__(self))

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

def split_escaped_delim (delimiter, string, count=0):
    """
    Returns the result of splitting ``string`` with ``delimiter``. It is an
    extension of ``string.split(delimiter, count)`` in that it ignores instances
    of the delimiter being escaped or contained within a string.

    :``delimiter``: The delimiter to split the string with. *Required*.
    :``string``: The string to be split. *Required*.
    :``count``: How many strings to limit the match to. *Default 0*.
    """
    assert len(delimiter) == 1

    split_expression = re.compile(r"""(?<!\\)%s""" % (delimiter))

    result = split_expression.split(string, count)

    return result

def parse_spec (spec_file):
    """
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
    """
    spec_object = None
    spec_name = spec_file.replace(".", "_")
    params = []
    default_params = {}
    int_conversion = []
    namedtuple = False
    delimiter = "\n"

    spec_file = open(spec_file, "r")
    spec = spec_file.readlines()
    spec_file.close()

    for line in spec:
        line = line.strip()
        param_name = None
        default_param = None
        if line.startswith("%id"):
            spec_name = line.split(" ", 1)[1]
        elif line.startswith("%delim"):
            delimiter = line.split(" ", 1)[1].strip()
        elif line.startswith("$"):
            line = line.split(" ", 1)
            if len(line) >= 1:
                param_name = line[0].strip("$")
            if len(line) == 2:
                default_param = line[1].strip()
            if param_name and not param_name.isdigit():
                namedtuple = True
            if default_param and param_name.isdigit():
                assert param_name != "0"
            params.append(param_name)
            if default_param:
                default_params[param_name]=default_param
        elif line.startswith("%int"):
            var = line.split(" ", 1)[1].strip()
            int_conversion.append(var)

    if namedtuple:
        class parent (object):
            def __init__ (self, *args, **kwargs):
                self.__name__ = spec_name
                if len(args) == len(params):
                    # arg for arg
                    for key, value in zip(params, args):
                        self.__dict__[key] = value
                elif len(kwargs) == len(params):
                    for key, value in kwargs.iteritems():
                        self.__dict__[key] = value
                else:
                    assert not "Didn't get the right number of arguments!"
            def __repr__ (self):
                values = ""
                for key in params:
                    values += "%s=%s," % (key, repr(self.__dict__[key]))
                return "<%s %s>" % (self.__name__, values.strip(", "))
    else:
        parent = list

    class spec_object (parent):
        def __init__ (self, block):
            self.__name__ = spec_name
            if isinstance(block, str):
                block = split_escaped_delim(delimiter, block.strip())
                assert len(block) + len(default_params) >= len(params)
                if len(block) < len(params):
                    for key, default in default_params.iteritems():
                        if key.isdigit():
                            assert int(key) >= len(block)
                            block.insert(int(key), default)
                        else:
                            block.append("%s=%s" % (key, default))

                if not namedtuple:
                    if int_conversion:
                        for conv in int_conversion:
                            block[conv] = int(block[conv])
                    parent.__init__(self, block)
                else:
                    new_data = {}
                    for item in block:
                        item = split_escaped_delim("=", item, 1)
                        if int_conversion and item[0] in int_conversion:
                            item[1] = int(item[1])
                        assert len(item) == 2
                        new_data[item[0]] = item[1]

                    parent.__init__(self, **new_data)
            elif isinstance(block, list):
                if not namedtuple:
                    parent.__init__(self, block)
                else:
                    parent.__init__(self, *block)
            elif isinstance(block, dict):
                assert namedtuple
                parent.__init__(self, **block)
        def __repr__ (self):
            if namedtuple:
                return parent.__repr__(self)
            else:
                return "<%s %s>" % (self.__name__, parent.__repr__(self))

    return spec_object

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
        spec = name + ".spec"
        if os.path.exists(os.path.join(data_path, spec)):
            spec_obj = parse_spec(os.path.join(data_path, spec))
        else:
            spec_obj = str
        dbfile = open(os.path.join(data_path, database), "r")
        dbdata = [spec_obj(item.strip()) for item in dbfile.read().strip().strip("%").split("%")]
        db = Database
        if hasattr(dbdata[0], 'weight'):
            db = WeightedDatabase
        globals()[name] = db(name, dbdata)
        dbfile.close()
        _dbobjects.append(globals()[name])

if __name__!="__main__":
    _do_build()
